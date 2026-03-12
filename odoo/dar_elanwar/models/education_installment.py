# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EducationInstallment(models.Model):
    _name = 'education.installment'
    _description = 'Installment'
    _order = 'subscription_id, sequence'

    subscription_id = fields.Many2one(
        'education.student.subscription',
        string='Subscription',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        related='subscription_id.student_id',
        store=True,
    )
    sequence = fields.Integer(
        string='Installment #',
        required=True,
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
    )
    amount = fields.Float(
        string='Amount',
        required=True,
    )
    paid_amount = fields.Float(
        string='Paid Amount',
        compute='_compute_paid_amount',
        store=True,
    )
    remaining_amount = fields.Float(
        string='Remaining',
        compute='_compute_remaining_amount',
        store=True,
    )
    is_paid = fields.Boolean(
        string='Paid',
        compute='_compute_is_paid',
        store=True,
    )
    paid_date = fields.Date(
        string='Paid Date',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='subscription_id.currency_id',
    )
    notes = fields.Text(
        string='Notes',
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Invoice',
        readonly=True,
        ondelete='set null',
        copy=False,
    )
    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Invoice Status',
        readonly=True,
        store=True,
    )

    # Related payments
    payment_ids = fields.One2many(
        'education.payment',
        'installment_id',
        string='Payments',
    )

    @api.depends('invoice_id.amount_total', 'invoice_id.amount_residual', 'invoice_id.state')
    def _compute_paid_amount(self):
        for record in self:
            if record.invoice_id and record.invoice_id.state == 'posted':
                record.paid_amount = record.invoice_id.amount_total - record.invoice_id.amount_residual
            else:
                record.paid_amount = 0.0

    @api.depends('amount', 'paid_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.amount - record.paid_amount

    @api.depends('amount', 'paid_amount')
    def _compute_is_paid(self):
        for record in self:
            record.is_paid = record.paid_amount >= record.amount

    # Computed counts for stat buttons
    payment_count = fields.Integer(
        string='Payments',
        compute='_compute_payment_count',
    )

    def _compute_payment_count(self):
        for record in self:
            record.payment_count = len(record.payment_ids)

    # Stat button actions
    def action_view_subscription(self):
        """View subscription"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscription',
            'res_model': 'education.student.subscription',
            'view_mode': 'form',
            'res_id': self.subscription_id.id,
        }

    def action_view_payments(self):
        """View installment payments"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('installment_id', '=', self.id)],
            'context': {'default_installment_id': self.id},
        }

    def action_view_student(self):
        """View student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'res_id': self.student_id.id,
        }

    def action_create_invoice(self):
        """Create a draft account.move invoice for this installment."""
        self.ensure_one()
        if self.invoice_id:
            raise UserError(_('Invoice already exists for this installment.'))

        student = self.student_id
        partner = student.father_id or student.mother_id or student

        income_account = self.env['account.account'].search(
            [('account_type', 'in', ('income', 'income_other'))],
            limit=1,
        )

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'ref': "Subscription: %s - Installment #%s" % (
                self.subscription_id.subscription_type_id.name or self.subscription_id.id,
                self.sequence,
            ),
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': "Subscription: %s - Installment #%s" % (
                    self.subscription_id.subscription_type_id.name or self.subscription_id.id,
                    self.sequence,
                ),
                'quantity': 1,
                'price_unit': self.amount,
                'account_id': income_account.id if income_account else False,
            })],
        }
        invoice = self.env['account.move'].create(invoice_vals)
        self.invoice_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice'),
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"Installment {record.sequence} - {record.student_id.name}"
            result.append((record.id, name))
        return result
