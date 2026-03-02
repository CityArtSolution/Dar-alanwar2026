# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

ATTENDANCE_STATUS = [
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
    ('excused', 'Excused'),
    ('leave', 'On Leave'),
]


class EducationEmployeeAttendance(models.Model):
    _name = 'education.employee.attendance'
    _description = 'Employee Attendance'
    _order = 'date desc, employee_id'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
    )
    check_in = fields.Float(
        string='Check In',
        help='Time in 24-hour format',
    )
    check_out = fields.Float(
        string='Check Out',
        help='Time in 24-hour format',
    )
    worked_hours = fields.Float(
        string='Worked Hours',
        compute='_compute_worked_hours',
        store=True,
    )
    status = fields.Selection(
        selection=ATTENDANCE_STATUS,
        string='Status',
        default='present',
        required=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    _sql_constraints = [
        ('employee_date_unique', 'UNIQUE(employee_id, date)',
         'Attendance record already exists for this employee on this date!'),
    ]

    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for record in self:
            if record.check_in and record.check_out and record.check_out > record.check_in:
                record.worked_hours = record.check_out - record.check_in
            else:
                record.worked_hours = 0.0

    @api.constrains('check_in', 'check_out')
    def _check_times(self):
        for record in self:
            if record.check_in and record.check_out:
                if record.check_out < record.check_in:
                    raise ValidationError('Check out time must be after check in time!')
            if record.check_in and (record.check_in < 0 or record.check_in > 24):
                raise ValidationError('Check in time must be between 0 and 24!')
            if record.check_out and (record.check_out < 0 or record.check_out > 24):
                raise ValidationError('Check out time must be between 0 and 24!')
