# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationProductCategory(models.Model):
    _name = 'education.product.category'
    _description = 'Product Category'
    _order = 'name'

    name = fields.Char(
        string='Category Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related products
    product_ids = fields.One2many(
        'education.product',
        'category_id',
        string='Products',
    )

    # Computed counts
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_counts',
    )
    total_quantity = fields.Float(
        string='Total Quantity',
        compute='_compute_counts',
    )
    total_value = fields.Float(
        string='Total Value',
        compute='_compute_counts',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Category code must be unique!'),
    ]

    @api.depends('product_ids', 'product_ids.quantity', 'product_ids.sale_price')
    def _compute_counts(self):
        for record in self:
            record.product_count = len(record.product_ids)
            record.total_quantity = sum(record.product_ids.mapped('quantity'))
            record.total_value = sum(p.quantity * p.sale_price for p in record.product_ids)

    # Stat button actions
    def action_view_products(self):
        """View products in this category"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'res_model': 'education.product',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }

    def action_view_stock_in(self):
        """View stock in records for products in this category"""
        self.ensure_one()
        product_ids = self.product_ids.ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock In',
            'res_model': 'education.stock.in',
            'view_mode': 'list,form',
            'domain': [('line_ids.product_id', 'in', product_ids)],
        }

    def action_view_stock_out(self):
        """View stock out records for products in this category"""
        self.ensure_one()
        product_ids = self.product_ids.ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Out',
            'res_model': 'education.stock.out',
            'view_mode': 'list,form',
            'domain': [('line_ids.product_id', 'in', product_ids)],
        }
