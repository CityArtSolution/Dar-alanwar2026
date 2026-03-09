from odoo import models, fields


class EducationSubscriptionType(models.Model):
    _name = 'education.subscription.type'
    _description = 'Subscription Type'

    name = fields.Char(string='Type Name', required=True)
    code = fields.Char(string='Code')
    department_id = fields.Many2one('education.department', string='Department')
    level_id = fields.Many2one('education.level', string='Level',
                                domain="[('department_id', '=', department_id)]")
    amount = fields.Float(string='Amount', required=True)
    payment_plan_id = fields.Many2one('education.payment.plan',
                                       string='Default Payment Plan')
    discount_ids = fields.Many2many('education.discount',
                                      'subscription_type_discount_rel',
                                      'type_id', 'discount_id',
                                      string='Applicable Discounts')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Subscription type code must be unique!'),
    ]
