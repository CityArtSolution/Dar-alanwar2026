# -*- coding: utf-8 -*-

from odoo import models, fields

PENALTY_TYPES = [
    ('warning', 'Warning'),
    ('deduction', 'Salary Deduction'),
    ('suspension', 'Suspension'),
    ('other', 'Other'),
]


class EducationEmployeePenalty(models.Model):
    _name = 'education.employee.penalty'
    _description = 'Employee Penalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    reason = fields.Text(
        string='Reason',
        required=True,
    )
    penalty_type = fields.Selection(
        selection=PENALTY_TYPES,
        string='Penalty Type',
        required=True,
        default='warning',
        tracking=True,
    )
    amount = fields.Float(
        string='Deduction Amount',
        help='Amount to deduct from salary (if applicable)',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    is_applied = fields.Boolean(
        string='Applied to Salary',
        default=False,
    )
    notes = fields.Text(
        string='Notes',
    )
    issued_by = fields.Many2one(
        'res.users',
        string='Issued By',
        default=lambda self: self.env.user,
    )
