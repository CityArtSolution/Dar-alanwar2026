from odoo import models, fields, api


class EducationPayment(models.Model):
    _name = 'education.payment'
    _description = 'Payment'
    _order = 'date desc'

    installment_id = fields.Many2one('education.installment', string='Installment',
                                      required=True, ondelete='cascade')
    student_id = fields.Many2one(related='installment_id.student_id',
                                  store=True, string='Student')
    date = fields.Date(string='Payment Date', required=True,
                        default=fields.Date.today)
    amount = fields.Float(string='Amount', required=True)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('card', 'Credit/Debit Card'),
        ('online', 'Online Payment'),
        ('cheque', 'Cheque'),
    ], string='Payment Method', default='cash')
    received_by = fields.Many2one('res.users', string='Received By',
                                   default=lambda self: self.env.user)
    reference = fields.Char(string='Reference')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            inst = rec.installment_id
            inst.paid_amount = sum(inst.payment_ids.mapped('amount'))
        return records
