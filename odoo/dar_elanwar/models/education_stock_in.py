# -*- coding: utf-8 -*-

from odoo import models, fields, api

STOCK_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]


class EducationStockIn(models.Model):
    _name = 'education.stock.in'
    _description = 'Stock In'
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
    supplier = fields.Char(
        string='Supplier',
    )
    invoice_reference = fields.Char(
        string='Invoice Reference',
    )
    state = fields.Selection(
        selection=STOCK_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total',
        store=True,
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

    # Lines
    line_ids = fields.One2many(
        'education.stock.in.line',
        'stock_in_id',
        string='Lines',
    )

    # Computed counts
    line_count = fields.Integer(
        string='Line Count',
        compute='_compute_counts',
    )
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_counts',
    )
    total_quantity = fields.Float(
        string='Total Quantity',
        compute='_compute_counts',
    )

    @api.depends('line_ids', 'line_ids.subtotal', 'line_ids.quantity')
    def _compute_counts(self):
        for record in self:
            record.line_count = len(record.line_ids)
            record.product_count = len(record.line_ids.mapped('product_id'))
            record.total_quantity = sum(record.line_ids.mapped('quantity'))

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.line_ids.mapped('subtotal'))

    # Stat button actions
    def action_view_lines(self):
        """View stock in lines"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock In Lines',
            'res_model': 'education.stock.in.line',
            'view_mode': 'list,form',
            'domain': [('stock_in_id', '=', self.id)],
            'context': {'default_stock_in_id': self.id},
        }

    def action_view_products(self):
        """View products in this stock in"""
        self.ensure_one()
        product_ids = self.line_ids.mapped('product_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'res_model': 'education.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', product_ids)],
        }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('education.stock.in') or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        """Confirm the stock in"""
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        """Cancel the stock in"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})


class EducationStockInLine(models.Model):
    _name = 'education.stock.in.line'
    _description = 'Stock In Line'
    _order = 'stock_in_id, id'

    stock_in_id = fields.Many2one(
        'education.stock.in',
        string='Stock In',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'education.product',
        string='Product',
        required=True,
    )
    quantity = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
    )
    unit_price = fields.Float(
        string='Unit Price',
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.quantity * record.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.purchase_price
