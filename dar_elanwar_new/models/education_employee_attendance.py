from odoo import models, fields, api


class EducationEmployeeAttendance(models.Model):
    _name = 'education.employee.attendance'
    _description = 'Employee Attendance'
    _order = 'date desc'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    check_in = fields.Float(string='Check In')
    check_out = fields.Float(string='Check Out')
    worked_hours = fields.Float(string='Worked Hours', compute='_compute_worked_hours',
                                 store=True)
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ], string='Status', default='present')

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out and rec.check_out > rec.check_in:
                rec.worked_hours = rec.check_out - rec.check_in
            else:
                rec.worked_hours = 0.0
