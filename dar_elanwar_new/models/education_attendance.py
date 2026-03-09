from odoo import models, fields, api


ATTENDANCE_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('locked', 'Locked'),
]


class EducationAttendance(models.Model):
    _name = 'education.attendance'
    _description = 'Student Attendance Sheet'
    _order = 'date desc'

    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    department_id = fields.Many2one('education.department', string='Department',
                                     required=True)
    class_id = fields.Many2one('education.class', string='Class',
                                domain="[('department_id', '=', department_id)]",
                                required=True)
    branch_id = fields.Many2one('education.branch', string='Branch')
    state = fields.Selection(ATTENDANCE_STATES, string='Status', default='draft')
    line_ids = fields.One2many('education.attendance.line', 'attendance_id',
                                string='Attendance Lines')

    present_count = fields.Integer(compute='_compute_counts', string='Present')
    absent_count = fields.Integer(compute='_compute_counts', string='Absent')
    late_count = fields.Integer(compute='_compute_counts', string='Late')

    @api.depends('line_ids.status')
    def _compute_counts(self):
        for rec in self:
            rec.present_count = len(rec.line_ids.filtered(
                lambda l: l.status == 'present'))
            rec.absent_count = len(rec.line_ids.filtered(
                lambda l: l.status == 'absent'))
            rec.late_count = len(rec.line_ids.filtered(
                lambda l: l.status == 'late'))

    def action_populate_students(self):
        """Fill in attendance lines with all students from the class."""
        for rec in self:
            existing_students = rec.line_ids.mapped('student_id')
            students = self.env['education.student'].search([
                ('class_id', '=', rec.class_id.id),
                ('state', '=', 'enrolled'),
            ])
            for student in students:
                if student not in existing_students:
                    self.env['education.attendance.line'].create({
                        'attendance_id': rec.id,
                        'student_id': student.id,
                        'status': 'present',
                    })

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_lock(self):
        self.write({'state': 'locked'})


class EducationAttendanceLine(models.Model):
    _name = 'education.attendance.line'
    _description = 'Student Attendance Line'

    attendance_id = fields.Many2one('education.attendance',
                                     string='Attendance Sheet',
                                     required=True, ondelete='cascade')
    student_id = fields.Many2one('education.student', string='Student',
                                  required=True)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ], string='Status', default='present', required=True)

    # PRD Gap Fields - Time tracking
    check_in_time = fields.Datetime(string='Check In Time')
    check_out_time = fields.Datetime(string='Check Out Time')
    hours_present = fields.Float(string='Hours Present',
                                  compute='_compute_hours_present', store=True)
    late_minutes = fields.Integer(string='Late Minutes',
                                   compute='_compute_late_minutes', store=True)

    @api.depends('check_in_time', 'check_out_time')
    def _compute_hours_present(self):
        for rec in self:
            if rec.check_in_time and rec.check_out_time:
                delta = rec.check_out_time - rec.check_in_time
                rec.hours_present = delta.total_seconds() / 3600.0
            else:
                rec.hours_present = 0.0

    @api.depends('check_in_time', 'attendance_id.class_id.schedule_id')
    def _compute_late_minutes(self):
        for rec in self:
            if (rec.check_in_time and rec.attendance_id.class_id.schedule_id):
                schedule = rec.attendance_id.class_id.schedule_id
                expected_hour = int(schedule.time_from)
                expected_min = int((schedule.time_from - expected_hour) * 60)
                actual = fields.Datetime.context_timestamp(rec, rec.check_in_time)
                expected_minutes = expected_hour * 60 + expected_min
                actual_minutes = actual.hour * 60 + actual.minute
                diff = actual_minutes - expected_minutes
                rec.late_minutes = max(0, diff)
            else:
                rec.late_minutes = 0
