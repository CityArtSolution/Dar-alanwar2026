from odoo import models, fields


class EducationPaymentPlan(models.Model):
    _name = 'education.payment.plan'
    _description = 'Payment Plan'

    name = fields.Char(string='Plan Name', required=True)
    installment_count = fields.Integer(string='Number of Installments',
                                        required=True)
    interval_months = fields.Integer(string='Interval (Months)', default=1)
    active = fields.Boolean(default=True)
