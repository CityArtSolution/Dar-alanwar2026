# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

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
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, id desc'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    name = fields.Char(
        string='Plan Name',
        required=True,
        tracking=True,
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
        tracking=True,
    )
    line_ids = fields.One2many(
        'education.financial.plan.line',
        'plan_id',
        string='Installment Lines',
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.depends('line_ids.amount', 'line_ids.is_paid', 'line_ids.discounted_amount')
    def _compute_amounts(self):
        for plan in self:
            lines = plan.line_ids
            plan.installment_count = len(lines)
            plan.paid_amount = sum(line.discounted_amount for line in lines if line.is_paid)
            plan.remaining_amount = sum(line.discounted_amount for line in lines if not line.is_paid)

    def action_generate_invoices(self):
        """Manual button to generate invoices for due lines."""
        self.ensure_one()
        created = self._generate_invoices_for_lines()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Invoice Generation',
                'message': '%d invoice(s) created.' % created,
                'type': 'success',
                'sticky': False,
            },
        }

    def _generate_invoices_for_lines(self):
        """Core logic: create draft account.move invoices for due plan lines."""
        today = fields.Date.today()
        created_count = 0
        income_account = self.env['account.account'].search(
            [('account_type', 'in', ('income', 'income_other'))],
            limit=1,
        )
        for plan in self:
            if plan.status != 'active':
                continue
            student = plan.student_id
            partner = student.father_id or student.mother_id or student
            due_lines = plan.line_ids.filtered(
                lambda l: l.due_date and l.due_date <= today and not l.invoice_id
            )
            for line in due_lines:
                invoice_vals = {
                    'move_type': 'out_invoice',
                    'partner_id': partner.id,
                    'ref': "Financial Plan: %s - Installment #%s" % (plan.name, line.sequence),
                    'invoice_date': today,
                    'invoice_line_ids': [(0, 0, {
                        'name': "Financial Plan: %s - Installment #%s" % (plan.name, line.sequence),
                        'quantity': 1,
                        'price_unit': line.discounted_amount,
                        'account_id': income_account.id if income_account else False,
                    })],
                }
                invoice = self.env['account.move'].create(invoice_vals)
                line.invoice_id = invoice.id
                created_count += 1
        return created_count

    @api.model
    def _cron_auto_generate_plan_invoices(self):
        """Cron: search all active plans and generate invoices for due lines."""
        plans = self.search([('status', '=', 'active')])
        if plans:
            count = plans._generate_invoices_for_lines()
            _logger.info('Financial Plan cron: created %d invoice(s).', count)


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

    # --- New fields for discount & invoice integration ---
    discount_id = fields.Many2one(
        'education.discount',
        string='Discount',
    )
    discounted_amount = fields.Float(
        string='Discounted Amount',
        compute='_compute_discounted_amount',
        store=True,
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        ondelete='set null',
    )
    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Invoice Status',
        readonly=True,
        store=True,
    )

    @api.depends('amount', 'discount_id', 'discount_id.value', 'discount_id.value_type')
    def _compute_discounted_amount(self):
        for line in self:
            if line.discount_id:
                if line.discount_id.value_type == 'percentage':
                    line.discounted_amount = line.amount * (1 - line.discount_id.value / 100)
                else:
                    line.discounted_amount = max(line.amount - line.discount_id.value, 0)
            else:
                line.discounted_amount = line.amount
