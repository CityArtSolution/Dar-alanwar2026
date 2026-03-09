# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationSubscriptionType(models.Model):
    _name = 'education.subscription.type'
    _description = 'Subscription Type'
    _order = 'department_id, name'

    name = fields.Char(
        string='Subscription Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
    )
    level_id = fields.Many2one(
        'education.level',
        string='Level',
        domain="[('department_id', '=', department_id)]",
    )
    amount = fields.Float(
        string='Amount',
        required=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    payment_plan_id = fields.Many2one(
        'education.payment.plan',
        string='Default Payment Plan',
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    discount_ids = fields.Many2many(
        'education.discount',
        'subscription_type_discount_rel',
        'type_id', 'discount_id',
        string='Applicable Discounts',
    )

    _code_uniq = models.Constraint(
        'unique(code)',
        'Subscription type code must be unique!',
    )

    # Related records
    subscription_ids = fields.One2many(
        'education.student.subscription',
        'subscription_type_id',
        string='Subscriptions',
    )

    # Computed counts
    subscription_count = fields.Integer(
        string='Subscription Count',
        compute='_compute_subscription_count',
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_subscription_count',
    )
    total_revenue = fields.Float(
        string='Total Revenue',
        compute='_compute_subscription_count',
    )

    @api.depends('subscription_ids', 'subscription_ids.net_amount')
    def _compute_subscription_count(self):
        for record in self:
            subscriptions = record.subscription_ids
            record.subscription_count = len(subscriptions)
            record.student_count = len(subscriptions.mapped('student_id'))
            record.total_revenue = sum(subscriptions.mapped('net_amount'))

    def action_view_subscriptions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('subscription_type_id', '=', self.id)],
            'context': {'default_subscription_type_id': self.id},
        }

    def action_view_students(self):
        self.ensure_one()
        student_ids = self.subscription_ids.mapped('student_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('id', 'in', student_ids)],
        }

    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.department_id:
                name = f"{record.department_id.name} / {record.name}"
            record.display_name = name
