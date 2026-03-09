# -*- coding: utf-8 -*-

from odoo import models, fields, api

PAYMENT_METHODS = [
    ('cash', 'Cash'),
    ('bank', 'Bank Transfer'),
    ('card', 'Card'),
    ('other', 'Other'),
]


class EducationPayment(models.Model):
    _name = 'education.payment'
    _description = 'Payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    installment_id = fields.Many2one(
        'education.installment',
        string='Installment',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        related='installment_id.student_id',
        store=True,
    )
    date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
        tracking=True,
    )
    payment_method = fields.Selection(
        selection=PAYMENT_METHODS,
        string='Payment Method',
        default='cash',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    received_by = fields.Many2one(
        'res.users',
        string='Received By',
        default=lambda self: self.env.user,
    )
    receipt_id = fields.Many2one(
        'education.payment.receipt',
        string='Receipt',
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Update installment paid amount
            installment = record.installment_id
            total_paid = sum(installment.payment_ids.mapped('amount'))
            installment.write({
                'paid_amount': total_paid,
                'paid_date': record.date if total_paid >= installment.amount else False,
            })
        return records
