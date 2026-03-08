# -*- coding: utf-8 -*-

from odoo import models, fields, api

ATTENDANCE_STATE = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('locked', 'Locked'),
]


class EducationAttendance(models.Model):
    _name = 'education.attendance'
    _description = 'Student Attendance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        required=True,
        domain="[('department_id', '=', department_id)]",
    )
    recorded_by = fields.Many2one(
        'res.users',
        string='Recorded By',
        default=lambda self: self.env.user,
    )
    state = fields.Selection(
        selection=ATTENDANCE_STATE,
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related records
    line_ids = fields.One2many(
        'education.attendance.line',
        'attendance_id',
        string='Attendance Lines',
    )

    # Computed
    present_count = fields.Integer(
        string='Present',
        compute='_compute_counts',
    )
    absent_count = fields.Integer(
        string='Absent',
        compute='_compute_counts',
    )
    late_count = fields.Integer(
        string='Late',
        compute='_compute_counts',
    )
    total_count = fields.Integer(
        string='Total',
        compute='_compute_counts',
    )

    _sql_constraints = [
        ('class_date_unique', 'UNIQUE(class_id, date)',
         'Attendance already exists for this class on this date!'),
    ]

    @api.depends('line_ids.status')
    def _compute_counts(self):
        for record in self:
            record.present_count = len(record.line_ids.filtered(lambda l: l.status == 'present'))
            record.absent_count = len(record.line_ids.filtered(lambda l: l.status == 'absent'))
            record.late_count = len(record.line_ids.filtered(lambda l: l.status == 'late'))
            record.total_count = len(record.line_ids)

    # Stat button actions
    def action_view_class(self):
        """View attendance class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'res_model': 'education.class',
            'view_mode': 'form',
            'res_id': self.class_id.id,
        }

    def action_view_present(self):
        """View present students"""
        self.ensure_one()
        present_lines = self.line_ids.filtered(lambda l: l.status == 'present')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Present Students',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('id', 'in', present_lines.mapped('student_id').ids)],
        }

    def action_view_absent(self):
        """View absent students"""
        self.ensure_one()
        absent_lines = self.line_ids.filtered(lambda l: l.status == 'absent')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Absent Students',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('id', 'in', absent_lines.mapped('student_id').ids)],
        }

    @api.onchange('class_id')
    def _onchange_class_id(self):
        """Load all students in the class as present by default"""
        if self.class_id:
            students = self.env['res.partner'].search([
                ('is_student', '=', True),
                ('class_id', '=', self.class_id.id),
                ('student_state', '=', 'enrolled'),
            ])
            lines = []
            for student in students:
                lines.append((0, 0, {
                    'student_id': student.id,
                    'status': 'present',
                }))
            self.line_ids = lines

    def action_confirm(self):
        """Confirm the attendance"""
        self.write({'state': 'confirmed'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})

    def action_mark_all_present(self):
        """Mark all students as present"""
        self.line_ids.write({'status': 'present'})

    def action_mark_all_absent(self):
        """Mark all students as absent"""
        self.line_ids.write({'status': 'absent'})

    def action_populate_students(self):
        """Fill in attendance lines with all students from the class."""
        for rec in self:
            existing_students = rec.line_ids.mapped('student_id')
            students = self.env['res.partner'].search([
                ('is_student', '=', True),
                ('class_id', '=', rec.class_id.id),
                ('student_state', '=', 'enrolled'),
            ])
            for student in students:
                if student not in existing_students:
                    self.env['education.attendance.line'].create({
                        'attendance_id': rec.id,
                        'student_id': student.id,
                        'status': 'present',
                    })

    def action_lock(self):
        """Lock the attendance"""
        self.write({'state': 'locked'})


class EducationAttendanceLine(models.Model):
    _name = 'education.attendance.line'
    _description = 'Attendance Line'
    _order = 'attendance_id, student_id'

    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    attendance_id = fields.Many2one(
        'education.attendance',
        string='Attendance',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        domain=[('is_student', '=', True)],
    )
    status = fields.Selection(
        selection=ATTENDANCE_STATUS,
        string='Status',
        default='present',
        required=True,
    )
    notes = fields.Char(
        string='Notes',
    )

    # PRD Gap Fields - Time tracking
    check_in_time = fields.Datetime(
        string='Check In Time',
    )
    check_out_time = fields.Datetime(
        string='Check Out Time',
    )
    hours_present = fields.Float(
        string='Hours Present',
        compute='_compute_hours_present',
        store=True,
    )
    late_minutes = fields.Integer(
        string='Late Minutes',
        compute='_compute_late_minutes',
        store=True,
    )

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
