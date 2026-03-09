from odoo import models, fields, api


class EducationEmployeeLoan(models.Model):
    _name = 'education.employee.loan'
    _description = 'Employee Loan'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    amount = fields.Float(string='Loan Amount', required=True)
    date = fields.Date(string='Loan Date', default=fields.Date.today)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paid', 'Fully Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    repayment_months = fields.Integer(string='Repayment Period (Months)')
    monthly_deduction = fields.Float(string='Monthly Deduction',
                                      compute='_compute_monthly_deduction',
                                      store=True)
    total_paid = fields.Float(string='Total Paid')
    remaining = fields.Float(string='Remaining', compute='_compute_remaining',
                              store=True)
    notes = fields.Text(string='Notes')

    @api.depends('amount', 'repayment_months')
    def _compute_monthly_deduction(self):
        for rec in self:
            if rec.repayment_months:
                rec.monthly_deduction = rec.amount / rec.repayment_months
            else:
                rec.monthly_deduction = 0.0

    @api.depends('amount', 'total_paid')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining = rec.amount - rec.total_paid

    def action_approve(self):
        self.write({'status': 'active'})

    def action_mark_paid(self):
        self.write({'status': 'paid'})
