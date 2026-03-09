# -*- coding: utf-8 -*-

from odoo import models, fields, api

TREASURY_STATES = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('closed', 'Closed'),
]


class EducationTreasury(models.Model):
    _name = 'education.treasury'
    _description = 'Daily Treasury'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
        required=True,
        tracking=True,
    )
    opening_balance = fields.Float(
        string='Opening Balance',
        required=True,
        tracking=True,
    )
    total_income = fields.Float(
        string='Total Income',
        compute='_compute_totals',
        store=True,
    )
    total_expense = fields.Float(
        string='Total Expense',
        compute='_compute_totals',
        store=True,
    )
    closing_balance = fields.Float(
        string='Closing Balance',
        compute='_compute_totals',
        store=True,
    )
    state = fields.Selection(
        selection=TREASURY_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user,
    )
    notes = fields.Text(
        string='Notes',
    )
    # Related transactions
    transaction_ids = fields.One2many(
        'education.transaction',
        'treasury_id',
        string='Transactions',
    )

    _date_branch_unique = models.Constraint(
        'UNIQUE(date, branch_id)',
        'Only one treasury per branch per day!',
    )

    # Computed counts for stat buttons
    transaction_count = fields.Integer(
        string='Transactions',
        compute='_compute_transaction_count',
    )
    income_count = fields.Integer(
        string='Income',
        compute='_compute_transaction_count',
    )
    expense_count = fields.Integer(
        string='Expense',
        compute='_compute_transaction_count',
    )

    def _compute_transaction_count(self):
        for record in self:
            record.transaction_count = len(record.transaction_ids)
            record.income_count = len(record.transaction_ids.filtered(lambda t: t.type == 'income'))
            record.expense_count = len(record.transaction_ids.filtered(lambda t: t.type == 'expense'))

    @api.depends('opening_balance', 'transaction_ids.amount', 'transaction_ids.type')
    def _compute_totals(self):
        for record in self:
            income = sum(record.transaction_ids.filtered(lambda t: t.type == 'income').mapped('amount'))
            expense = sum(record.transaction_ids.filtered(lambda t: t.type == 'expense').mapped('amount'))
            record.total_income = income
            record.total_expense = expense
            record.closing_balance = record.opening_balance + income - expense

    # Stat button actions
    def action_view_transactions(self):
        """View all transactions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transactions',
            'res_model': 'education.transaction',
            'view_mode': 'list,form',
            'domain': [('treasury_id', '=', self.id)],
            'context': {'default_treasury_id': self.id},
        }

    def action_view_income(self):
        """View income transactions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Income',
            'res_model': 'education.transaction',
            'view_mode': 'list,form',
            'domain': [('treasury_id', '=', self.id), ('type', '=', 'income')],
            'context': {'default_treasury_id': self.id, 'default_type': 'income'},
        }

    def action_view_expense(self):
        """View expense transactions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expense',
            'res_model': 'education.transaction',
            'view_mode': 'list,form',
            'domain': [('treasury_id', '=', self.id), ('type', '=', 'expense')],
            'context': {'default_treasury_id': self.id, 'default_type': 'expense'},
        }

    def action_view_branch(self):
        """View treasury branch"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Branch',
            'res_model': 'education.branch',
            'view_mode': 'form',
            'res_id': self.branch_id.id,
        }

    def action_open(self):
        """Open the treasury for the day"""
        self.write({'state': 'open'})

    def action_close(self):
        """Close the treasury for the day"""
        self.write({'state': 'closed'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})

    def _compute_display_name(self):
        for record in self:
            name = f"Treasury - {record.branch_id.name} - {record.date}"
            record.display_name = name
