# -*- coding: utf-8 -*-

from odoo import models, fields, api

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

PAYMENT_METHODS = [
    ('cash', 'Cash'),
    ('bank', 'Bank Transfer'),
    ('card', 'Card'),
    ('check', 'Check'),
    ('other', 'Other'),
]


class EducationTransaction(models.Model):
    _name = 'education.transaction'
    _description = 'Treasury Transaction'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New',
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    treasury_id = fields.Many2one(
        'education.treasury',
        string='Treasury',
        domain="[('date', '=', date), ('state', '=', 'open')]",
    )
    type = fields.Selection(
        selection=TRANSACTION_TYPES,
        string='Type',
        required=True,
        tracking=True,
    )
    category_id = fields.Many2one(
        'education.transaction.category',
        string='Category',
        required=True,
        domain="[('type', '=', type)]",
    )
    amount = fields.Float(
        string='Amount',
        required=True,
        tracking=True,
    )
    payment_method = fields.Selection(
        selection=PAYMENT_METHODS,
        string='Payment Method',
        default='cash',
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    reference = fields.Char(
        string='External Reference',
        help='External document reference (invoice, receipt, etc.)',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Recorded By',
        default=lambda self: self.env.user,
    )
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
        related='treasury_id.branch_id',
        store=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related to other modules (optional links)
    student_id = fields.Many2one(
        'education.student',
        string='Related Student',
    )
    employee_id = fields.Many2one(
        'education.employee',
        string='Related Employee',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                prefix = 'INC/' if vals.get('type') == 'income' else 'EXP/'
                vals['name'] = self.env['ir.sequence'].next_by_code('education.transaction') or 'New'
                vals['name'] = prefix + vals['name']
        return super().create(vals_list)
