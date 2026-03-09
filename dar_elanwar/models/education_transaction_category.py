# -*- coding: utf-8 -*-

from odoo import models, fields, api

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]


class EducationTransactionCategory(models.Model):
    _name = 'education.transaction.category'
    _description = 'Transaction Category'
    _order = 'type, name'

    name = fields.Char(
        string='Category Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    type = fields.Selection(
        selection=TRANSACTION_TYPES,
        string='Type',
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    transaction_ids = fields.One2many(
        'education.transaction',
        'category_id',
        string='Transactions',
    )

    # Computed counts
    transaction_count = fields.Integer(
        string='Transaction Count',
        compute='_compute_transaction_count',
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_transaction_count',
    )

    @api.depends('transaction_ids', 'transaction_ids.amount')
    def _compute_transaction_count(self):
        for record in self:
            record.transaction_count = len(record.transaction_ids)
            record.total_amount = sum(record.transaction_ids.mapped('amount'))

    def action_view_transactions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transactions',
            'res_model': 'education.transaction',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }

    _code_type_unique = models.Constraint(
        'UNIQUE(code, type)',
        'Code must be unique per type!',
    )

    def _compute_display_name(self):
        for record in self:
            type_label = dict(TRANSACTION_TYPES).get(record.type, record.type)
            name = f"[{record.code}] {record.name} ({type_label})"
            record.display_name = name
