from odoo import models, fields, api, _


class EducationPaymentReceipt(models.Model):
    _name = 'education.payment.receipt'
    _description = 'Payment Receipt'
    _order = 'date desc'

    receipt_number = fields.Char(string='Receipt Number', readonly=True,
                                  copy=False, default=lambda self: _('New'))
    student_id = fields.Many2one('education.student', string='Student',
                                  required=True)
    installment_id = fields.Many2one('education.installment',
                                      string='Installment')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    total_amount = fields.Float(string='Total Amount')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('receipt_number', _('New')) == _('New'):
                vals['receipt_number'] = self.env['ir.sequence'].next_by_code(
                    'education.payment.receipt') or _('New')
        return super().create(vals_list)
