from odoo import models, fields, api, _


class EducationTreasury(models.Model):
    _name = 'education.treasury'
    _description = 'Treasury Account'
    _inherit = ['mail.thread']

    name = fields.Char(string='Account Name', required=True)
    code = fields.Char(string='Code')
    branch_id = fields.Many2one('education.branch', string='Branch')
    balance = fields.Float(compute='_compute_balance', string='Balance',
                            store=True)
    transaction_ids = fields.One2many('education.treasury.transaction',
                                       'treasury_id', string='Transactions')
    active = fields.Boolean(default=True)

    @api.depends('transaction_ids.amount', 'transaction_ids.transaction_type')
    def _compute_balance(self):
        for rec in self:
            income = sum(rec.transaction_ids.filtered(
                lambda t: t.transaction_type == 'income').mapped('amount'))
            expense = sum(rec.transaction_ids.filtered(
                lambda t: t.transaction_type == 'expense').mapped('amount'))
            rec.balance = income - expense


class EducationTreasuryTransaction(models.Model):
    _name = 'education.treasury.transaction'
    _description = 'Treasury Transaction'
    _order = 'date desc'

    treasury_id = fields.Many2one('education.treasury', string='Treasury',
                                   required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    description = fields.Char(string='Description', required=True)
    transaction_type = fields.Selection([
        ('income', 'Income'),
        ('expense', 'Expense'),
    ], string='Type', required=True)
    amount = fields.Float(string='Amount', required=True)
    reference = fields.Char(string='Reference')
    category = fields.Selection([
        ('tuition', 'Tuition'),
        ('salary', 'Salary'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ], string='Category')
    notes = fields.Text(string='Notes')


class EducationExpense(models.Model):
    _name = 'education.expense'
    _description = 'Expense Record'
    _order = 'date desc'

    name = fields.Char(string='Description', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    amount = fields.Float(string='Amount', required=True)
    category = fields.Selection([
        ('salary', 'Salary'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('utilities', 'Utilities'),
        ('rent', 'Rent'),
        ('other', 'Other'),
    ], string='Category')
    branch_id = fields.Many2one('education.branch', string='Branch')
    treasury_id = fields.Many2one('education.treasury', string='Treasury')
    notes = fields.Text(string='Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], string='Status', default='draft')
