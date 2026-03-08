# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

SUBSCRIPTION_STATUS = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('cancelled', 'Cancelled'),
]


class EducationStudentSubscription(models.Model):
    _name = 'education.student.subscription'
    _description = 'Student Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        ondelete='cascade',
        tracking=True,
        domain=[('is_student', '=', True)],
    )
    subscription_type_id = fields.Many2one(
        'education.subscription.type',
        string='Subscription Type',
        required=True,
        tracking=True,
    )
    payment_plan_id = fields.Many2one(
        'education.payment.plan',
        string='Payment Plan',
        required=True,
        tracking=True,
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    end_date = fields.Date(
        string='End Date',
        tracking=True,
    )
    total_amount = fields.Float(
        string='Total Amount',
        required=True,
        tracking=True,
    )
    discount = fields.Float(
        string='Discount',
        default=0.0,
    )
    discount_id = fields.Many2one(
        'education.discount',
        string='Discount Applied',
    )
    discount_type = fields.Selection([
        ('sibling', 'Sibling'),
        ('early_payment', 'Early Payment'),
        ('scholarship', 'Scholarship'),
        ('custom', 'Custom'),
    ], string='Discount Type', related='discount_id.discount_type', store=True)
    discount_amount = fields.Float(
        string='Discount Amount',
        compute='_compute_discount_amount',
        store=True,
    )
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
    )
    net_amount = fields.Float(
        string='Net Amount',
        compute='_compute_net_amount',
        store=True,
    )
    paid_amount = fields.Float(
        string='Paid Amount',
        compute='_compute_paid_amount',
        store=True,
    )
    remaining_amount = fields.Float(
        string='Remaining Amount',
        compute='_compute_remaining_amount',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    status = fields.Selection(
        selection=SUBSCRIPTION_STATUS,
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related records
    installment_ids = fields.One2many(
        'education.installment',
        'subscription_id',
        string='Installments',
    )

    # Computed counts for stat buttons
    installment_count = fields.Integer(
        string='Installments',
        compute='_compute_stat_counts',
    )
    payment_count = fields.Integer(
        string='Payments',
        compute='_compute_stat_counts',
    )

    def _compute_stat_counts(self):
        for record in self:
            record.installment_count = len(record.installment_ids)
            record.payment_count = self.env['education.payment'].search_count([
                ('installment_id', 'in', record.installment_ids.ids)
            ])

    # Stat button actions
    def action_view_installments(self):
        """View subscription installments"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installments',
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id', '=', self.id)],
            'context': {'default_subscription_id': self.id},
        }

    def action_view_payments(self):
        """View subscription payments"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('installment_id', 'in', self.installment_ids.ids)],
        }

    def action_view_student(self):
        """View associated student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': self.student_id.id,
        }

    @api.depends('total_amount', 'discount')
    def _compute_net_amount(self):
        for record in self:
            record.net_amount = record.total_amount - record.discount

    @api.depends('installment_ids.paid_amount')
    def _compute_paid_amount(self):
        for record in self:
            record.paid_amount = sum(record.installment_ids.mapped('paid_amount'))

    @api.depends('net_amount', 'paid_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.net_amount - record.paid_amount

    @api.onchange('subscription_type_id')
    def _onchange_subscription_type_id(self):
        if self.subscription_type_id:
            self.total_amount = self.subscription_type_id.amount
            if self.subscription_type_id.payment_plan_id:
                self.payment_plan_id = self.subscription_type_id.payment_plan_id

    def action_generate_installments(self):
        """Generate installments based on payment plan"""
        self.ensure_one()
        if not self.payment_plan_id:
            return

        # Delete existing installments
        self.installment_ids.unlink()

        installment_amount = self.net_amount / self.payment_plan_id.installment_count
        due_date = self.start_date

        for i in range(self.payment_plan_id.installment_count):
            self.env['education.installment'].create({
                'subscription_id': self.id,
                'sequence': i + 1,
                'due_date': due_date,
                'amount': installment_amount,
            })
            due_date = due_date + relativedelta(months=self.payment_plan_id.interval_months)

        self.write({'status': 'active'})

    def action_cancel(self):
        """Cancel the subscription"""
        self.write({'status': 'cancelled'})

    def action_expire(self):
        """Mark as expired"""
        self.write({'status': 'expired'})

    @api.depends('total_amount', 'discount_id', 'discount_id.value',
                 'discount_id.value_type')
    def _compute_discount_amount(self):
        for rec in self:
            if rec.discount_id:
                if rec.discount_id.value_type == 'percentage':
                    rec.discount_amount = rec.total_amount * rec.discount_id.value / 100
                else:
                    rec.discount_amount = rec.discount_id.value
            else:
                rec.discount_amount = 0.0

    @api.model
    def _cron_auto_generate_invoices(self):
        """Cron job to auto-create draft invoices from active subscriptions."""
        active_subs = self.search([('status', '=', 'active')])
        for sub in active_subs:
            overdue = sub.installment_ids.filtered(
                lambda i: not i.is_paid and i.due_date <= fields.Date.today())
            for inst in overdue:
                existing = self.env['education.payment.receipt'].search([
                    ('student_id', '=', sub.student_id.id),
                    ('installment_id', '=', inst.id),
                ], limit=1)
                if not existing:
                    self.env['education.payment.receipt'].create({
                        'student_id': sub.student_id.id,
                        'date': fields.Date.today(),
                        'total_amount': inst.amount - inst.paid_amount,
                        'installment_id': inst.id,
                    })

    def _auto_apply_sibling_discount(self):
        """Auto-apply sibling discount when enrolling students with same parent."""
        for sub in self:
            student = sub.student_id
            parent = student.father_id or student.mother_id
            if not parent:
                continue
            siblings = parent._get_all_children().filtered(
                lambda s: s.id != student.id and s.student_state == 'enrolled')
            if len(siblings) >= 1:
                sibling_discount = self.env['education.discount'].search([
                    ('discount_type', '=', 'sibling'),
                    ('auto_apply', '=', True),
                    ('active', '=', True),
                    '|',
                    ('department_id', '=', False),
                    ('department_id', '=', student.department_id.id),
                ], limit=1)
                if sibling_discount and not sub.discount_id:
                    sub.discount_id = sibling_discount.id
