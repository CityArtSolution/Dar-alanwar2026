# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationProduct(models.Model):
    _name = 'education.product'
    _description = 'Product/Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Product Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    category_id = fields.Many2one(
        'education.product.category',
        string='Category',
        required=True,
    )
    unit = fields.Char(
        string='Unit',
        default='Piece',
    )
    purchase_price = fields.Float(
        string='Purchase Price',
    )
    sale_price = fields.Float(
        string='Sale Price',
    )
    quantity = fields.Float(
        string='Quantity On Hand',
        compute='_compute_quantity',
        store=True,
    )
    min_quantity = fields.Float(
        string='Minimum Quantity',
        default=0.0,
        help='Minimum quantity before reorder',
    )
    description = fields.Text(
        string='Description',
    )
    image = fields.Binary(
        string='Image',
        attachment=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Stock movements
    stock_in_line_ids = fields.One2many(
        'education.stock.in.line',
        'product_id',
        string='Stock In Lines',
    )
    stock_out_line_ids = fields.One2many(
        'education.stock.out.line',
        'product_id',
        string='Stock Out Lines',
    )

    # Computed counts
    stock_in_count = fields.Integer(
        string='Stock In Count',
        compute='_compute_movement_counts',
    )
    stock_out_count = fields.Integer(
        string='Stock Out Count',
        compute='_compute_movement_counts',
    )
    total_in = fields.Float(
        string='Total In',
        compute='_compute_movement_counts',
    )
    total_out = fields.Float(
        string='Total Out',
        compute='_compute_movement_counts',
    )

    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Product code must be unique!',
    )

    @api.depends('stock_in_line_ids', 'stock_out_line_ids')
    def _compute_movement_counts(self):
        for record in self:
            confirmed_in = record.stock_in_line_ids.filtered(
                lambda l: l.stock_in_id.state == 'confirmed')
            confirmed_out = record.stock_out_line_ids.filtered(
                lambda l: l.stock_out_id.state == 'confirmed')
            record.stock_in_count = len(record.stock_in_line_ids)
            record.stock_out_count = len(record.stock_out_line_ids)
            record.total_in = sum(confirmed_in.mapped('quantity'))
            record.total_out = sum(confirmed_out.mapped('quantity'))

    @api.depends('stock_in_line_ids.quantity', 'stock_out_line_ids.quantity',
                 'stock_in_line_ids.stock_in_id.state', 'stock_out_line_ids.stock_out_id.state')
    def _compute_quantity(self):
        for record in self:
            # Sum confirmed stock ins
            stock_in = sum(record.stock_in_line_ids.filtered(
                lambda l: l.stock_in_id.state == 'confirmed'
            ).mapped('quantity'))
            # Sum confirmed stock outs
            stock_out = sum(record.stock_out_line_ids.filtered(
                lambda l: l.stock_out_id.state == 'confirmed'
            ).mapped('quantity'))
            record.quantity = stock_in - stock_out

    # Stat button actions
    def action_view_stock_in(self):
        """View stock in records for this product"""
        self.ensure_one()
        stock_in_ids = self.stock_in_line_ids.mapped('stock_in_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock In',
            'res_model': 'education.stock.in',
            'view_mode': 'list,form',
            'domain': [('id', 'in', stock_in_ids)],
        }

    def action_view_stock_out(self):
        """View stock out records for this product"""
        self.ensure_one()
        stock_out_ids = self.stock_out_line_ids.mapped('stock_out_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Out',
            'res_model': 'education.stock.out',
            'view_mode': 'list,form',
            'domain': [('id', 'in', stock_out_ids)],
        }

    def action_view_category(self):
        """View the product category"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Category',
            'res_model': 'education.product.category',
            'view_mode': 'form',
            'res_id': self.category_id.id,
        }

    def _compute_display_name(self):
        for record in self:
            name = f"[{record.code}] {record.name}"
            record.display_name = name
