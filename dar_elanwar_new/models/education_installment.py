from odoo import models, fields, api


class EducationInstallment(models.Model):
    _name = 'education.installment'
    _description = 'Installment'
    _order = 'due_date'

    subscription_id = fields.Many2one('education.student.subscription',
                                       string='Subscription', required=True,
                                       ondelete='cascade')
    student_id = fields.Many2one(related='subscription_id.student_id',
                                  store=True, string='Student')
    sequence = fields.Integer(string='#', default=1)
    due_date = fields.Date(string='Due Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    paid_amount = fields.Float(string='Paid Amount', default=0.0)
    is_paid = fields.Boolean(string='Paid', compute='_compute_is_paid',
                              store=True)
    payment_ids = fields.One2many('education.payment', 'installment_id',
                                   string='Payments')

    @api.depends('amount', 'paid_amount')
    def _compute_is_paid(self):
        for rec in self:
            rec.is_paid = rec.paid_amount >= rec.amount and rec.amount > 0
