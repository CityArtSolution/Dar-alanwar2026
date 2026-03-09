# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
        default=0.0,
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

    # Related payments
    payment_ids = fields.One2many(
        'education.payment',
        'installment_id',
        string='Payments',
    )

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

    def _compute_display_name(self):
        for record in self:
            name = f"Installment {record.sequence} - {record.student_id.name}"
            record.display_name = name
