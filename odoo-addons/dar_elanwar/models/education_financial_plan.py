# -*- coding: utf-8 -*-

from odoo import models, fields, api

FINANCIAL_PLAN_STATES = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('paid', 'Paid'),
    ('overdue', 'Overdue'),
    ('cancelled', 'Cancelled'),
]


class EducationFinancialPlan(models.Model):
    _name = 'education.financial.plan'
    _description = 'Financial Plan'
    _order = 'start_date desc, id desc'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Plan Name',
        required=True,
    )
    subscription_id = fields.Many2one(
        'education.student.subscription',
        string='Linked Subscription',
        domain="[('student_id', '=', student_id)]",
    )
    total_amount = fields.Float(
        string='Total Amount',
    )
    paid_amount = fields.Float(
        string='Paid Amount',
        compute='_compute_amounts',
        store=True,
    )
    remaining_amount = fields.Float(
        string='Remaining Amount',
        compute='_compute_amounts',
        store=True,
    )
    installment_count = fields.Integer(
        string='Number of Installments',
        compute='_compute_amounts',
        store=True,
    )
    start_date = fields.Date(
        string='Start Date',
    )
    end_date = fields.Date(
        string='End Date',
    )
    status = fields.Selection(
        FINANCIAL_PLAN_STATES,
        string='Status',
        default='draft',
    )
    line_ids = fields.One2many(
        'education.financial.plan.line',
        'plan_id',
        string='Installment Lines',
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.depends('line_ids.amount', 'line_ids.is_paid')
    def _compute_amounts(self):
        for plan in self:
            lines = plan.line_ids
            plan.installment_count = len(lines)
            plan.paid_amount = sum(line.amount for line in lines if line.is_paid)
            plan.remaining_amount = sum(line.amount for line in lines if not line.is_paid)


class EducationFinancialPlanLine(models.Model):
    _name = 'education.financial.plan.line'
    _description = 'Financial Plan Installment Line'
    _order = 'due_date, sequence'

    plan_id = fields.Many2one(
        'education.financial.plan',
        string='Financial Plan',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='#',
        default=10,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
    )
    due_date = fields.Date(
        string='Due Date',
    )
    is_paid = fields.Boolean(
        string='Paid',
        default=False,
    )
    payment_date = fields.Date(
        string='Payment Date',
    )
    notes = fields.Text(
        string='Notes',
    )
