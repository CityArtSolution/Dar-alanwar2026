# -*- coding: utf-8 -*-

from odoo import models, fields, api

LOAN_STATUS = [
    ('draft', 'Draft'),
    ('requested', 'Requested'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('paid', 'Paid'),
    ('repaying', 'Repaying'),
    ('completed', 'Completed'),
]


class EducationEmployeeLoan(models.Model):
    _name = 'education.employee.loan'
    _description = 'Employee Loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'request_date desc'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    request_date = fields.Date(
        string='Request Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    amount = fields.Float(
        string='Loan Amount',
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    reason = fields.Text(
        string='Reason',
    )
    status = fields.Selection(
        selection=LOAN_STATUS,
        string='Status',
        default='draft',
        tracking=True,
    )
    approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
    )
    approval_date = fields.Date(
        string='Approval Date',
    )
    paid_date = fields.Date(
        string='Paid Date',
    )
    repayment_months = fields.Integer(
        string='Repayment Months',
        default=1,
        help='Number of months to deduct from salary',
    )
    monthly_deduction = fields.Float(
        string='Monthly Deduction',
        compute='_compute_monthly_deduction',
        store=True,
    )
    remaining_amount = fields.Float(
        string='Remaining Amount',
        default=0.0,
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.depends('amount', 'repayment_months')
    def _compute_monthly_deduction(self):
        for record in self:
            if record.repayment_months > 0:
                record.monthly_deduction = record.amount / record.repayment_months
            else:
                record.monthly_deduction = record.amount

    def action_request(self):
        """Submit loan request"""
        self.write({'status': 'requested'})

    def action_approve(self):
        """Approve the loan"""
        self.write({
            'status': 'approved',
            'approved_by': self.env.user.id,
            'approval_date': fields.Date.today(),
        })

    def action_reject(self):
        """Reject the loan"""
        self.write({'status': 'rejected'})

    def action_pay(self):
        """Mark loan as paid to employee"""
        self.write({
            'status': 'repaying',
            'paid_date': fields.Date.today(),
            'remaining_amount': self.amount,
        })

    def action_complete(self):
        """Mark loan as fully repaid"""
        self.write({
            'status': 'completed',
            'remaining_amount': 0.0,
        })
