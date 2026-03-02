# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationPaymentReceipt(models.Model):
    _name = 'education.payment.receipt'
    _description = 'Payment Receipt'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, receipt_number desc'

    receipt_number = fields.Char(
        string='Receipt Number',
        readonly=True,
        copy=False,
        default='New',
    )
    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
        tracking=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    payment_ids = fields.One2many(
        'education.payment',
        'receipt_id',
        string='Payments',
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    issued_by = fields.Many2one(
        'res.users',
        string='Issued By',
        default=lambda self: self.env.user,
    )
    notes = fields.Text(
        string='Notes',
    )

    _sql_constraints = [
        ('receipt_number_unique', 'UNIQUE(receipt_number)', 'Receipt number must be unique!'),
    ]

    # Computed counts
    payment_count = fields.Integer(
        string='Payment Count',
        compute='_compute_counts',
    )
    installment_count = fields.Integer(
        string='Installment Count',
        compute='_compute_counts',
    )
    subscription_count = fields.Integer(
        string='Subscription Count',
        compute='_compute_counts',
    )

    @api.depends('payment_ids')
    def _compute_counts(self):
        for record in self:
            record.payment_count = len(record.payment_ids)
            installments = record.payment_ids.mapped('installment_id')
            record.installment_count = len(installments)
            subscriptions = installments.mapped('subscription_id')
            record.subscription_count = len(subscriptions)

    @api.depends('payment_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(record.payment_ids.mapped('amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('receipt_number', 'New') == 'New':
                vals['receipt_number'] = self.env['ir.sequence'].next_by_code('education.payment.receipt') or 'New'
        return super().create(vals_list)

    # Stat button actions
    def action_view_payments(self):
        """View payments in this receipt"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('receipt_id', '=', self.id)],
            'context': {'default_receipt_id': self.id},
        }

    def action_view_student(self):
        """View the student for this receipt"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'res_model': 'education.student',
            'view_mode': 'form',
            'res_id': self.student_id.id,
        }

    def action_view_installments(self):
        """View installments paid in this receipt"""
        self.ensure_one()
        installment_ids = self.payment_ids.mapped('installment_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Installments',
            'res_model': 'education.subscription.installment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', installment_ids)],
        }

    def action_view_subscriptions(self):
        """View subscriptions related to this receipt"""
        self.ensure_one()
        subscription_ids = self.payment_ids.mapped('installment_id.subscription_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('id', 'in', subscription_ids)],
        }
