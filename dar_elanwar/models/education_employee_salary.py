# -*- coding: utf-8 -*-

from odoo import models, fields, api

SALARY_STATUS = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled'),
]

MONTHS = [
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
]


class EducationEmployeeSalary(models.Model):
    _name = 'education.employee.salary'
    _description = 'Employee Salary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'year desc, month desc, employee_id'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    month = fields.Selection(
        selection=MONTHS,
        string='Month',
        required=True,
        tracking=True,
    )
    year = fields.Char(
        string='Year',
        required=True,
        default=lambda self: str(fields.Date.today().year),
        tracking=True,
    )
    basic_salary = fields.Float(
        string='Basic Salary',
        required=True,
    )
    bonuses = fields.Float(
        string='Bonuses',
        default=0.0,
    )
    deductions = fields.Float(
        string='Deductions',
        default=0.0,
    )
    loan_deduction = fields.Float(
        string='Loan Deduction',
        default=0.0,
    )
    penalty_deduction = fields.Float(
        string='Penalty Deduction',
        default=0.0,
    )
    net_salary = fields.Float(
        string='Net Salary',
        compute='_compute_net_salary',
        store=True,
    )
    state = fields.Selection(
        selection=SALARY_STATUS,
        string='Status',
        default='draft',
        tracking=True,
    )
    paid_date = fields.Date(
        string='Paid Date',
    )
    paid_by = fields.Many2one(
        'res.users',
        string='Paid By',
    )
    notes = fields.Text(
        string='Notes',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    _employee_month_year_unique = models.Constraint(
        'UNIQUE(employee_id, month, year)',
        'Salary record already exists for this employee for this period!',
    )

    @api.depends('basic_salary', 'bonuses', 'deductions', 'loan_deduction', 'penalty_deduction')
    def _compute_net_salary(self):
        for record in self:
            total_deductions = record.deductions + record.loan_deduction + record.penalty_deduction
            record.net_salary = record.basic_salary + record.bonuses - total_deductions

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.basic_salary = self.employee_id.salary

    def action_confirm(self):
        """Confirm the salary"""
        self.write({'state': 'confirmed'})

    def action_pay(self):
        """Mark salary as paid"""
        self.write({
            'state': 'paid',
            'paid_date': fields.Date.today(),
            'paid_by': self.env.user.id,
        })

    def action_cancel(self):
        """Cancel the salary"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft', 'paid_date': False, 'paid_by': False})
