# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationPaymentPlan(models.Model):
    _name = 'education.payment.plan'
    _description = 'Payment Plan'
    _order = 'sequence, name'

    name = fields.Char(
        string='Plan Name',
        required=True,
    )
    installment_count = fields.Integer(
        string='Number of Installments',
        required=True,
        default=1,
    )
    interval_months = fields.Integer(
        string='Interval (Months)',
        default=1,
        help='Number of months between installments',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    subscription_ids = fields.One2many(
        'education.student.subscription',
        'payment_plan_id',
        string='Subscriptions',
    )
    subscription_type_ids = fields.One2many(
        'education.subscription.type',
        'payment_plan_id',
        string='Subscription Types',
    )

    # Computed counts
    subscription_count = fields.Integer(
        string='Subscription Count',
        compute='_compute_counts',
    )
    subscription_type_count = fields.Integer(
        string='Type Count',
        compute='_compute_counts',
    )

    @api.depends('subscription_ids', 'subscription_type_ids')
    def _compute_counts(self):
        for record in self:
            record.subscription_count = len(record.subscription_ids)
            record.subscription_type_count = len(record.subscription_type_ids)

    def action_view_subscriptions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('payment_plan_id', '=', self.id)],
            'context': {'default_payment_plan_id': self.id},
        }

    def action_view_subscription_types(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscription Types',
            'res_model': 'education.subscription.type',
            'view_mode': 'list,form',
            'domain': [('payment_plan_id', '=', self.id)],
            'context': {'default_payment_plan_id': self.id},
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Payment plan name must be unique!'),
    ]
