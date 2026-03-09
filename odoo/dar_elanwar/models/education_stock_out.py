# -*- coding: utf-8 -*-

from odoo import models, fields, api

STOCK_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]


class EducationStockOut(models.Model):
    _name = 'education.stock.out'
    _description = 'Stock Out'
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
    recipient = fields.Char(
        string='Recipient',
        help='Person or department receiving the items',
    )
    reason = fields.Char(
        string='Reason',
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
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        help='If stock out is for a student',
    )
    notes = fields.Text(
        string='Notes',
    )

    # Lines
    line_ids = fields.One2many(
        'education.stock.out.line',
        'stock_out_id',
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
        """View stock out lines"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Out Lines',
            'res_model': 'education.stock.out.line',
            'view_mode': 'list,form',
            'domain': [('stock_out_id', '=', self.id)],
            'context': {'default_stock_out_id': self.id},
        }

    def action_view_products(self):
        """View products in this stock out"""
        self.ensure_one()
        product_ids = self.line_ids.mapped('product_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Products',
            'res_model': 'education.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', product_ids)],
        }

    def action_view_student(self):
        """View the student receiving stock"""
        self.ensure_one()
        if self.student_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Student',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.student_id.id,
            }

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('education.stock.out') or 'New'
        return super().create(vals_list)

    def action_confirm(self):
        """Confirm the stock out"""
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        """Cancel the stock out"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})


class EducationStockOutLine(models.Model):
    _name = 'education.stock.out.line'
    _description = 'Stock Out Line'
    _order = 'stock_out_id, id'

    stock_out_id = fields.Many2one(
        'education.stock.out',
        string='Stock Out',
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
            self.unit_price = self.product_id.sale_price
