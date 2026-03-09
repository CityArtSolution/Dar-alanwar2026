from odoo import models, fields, api, _


class EducationInventoryCategory(models.Model):
    _name = 'education.inventory.category'
    _description = 'Inventory Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Code')
    parent_id = fields.Many2one('education.inventory.category',
                                 string='Parent Category')
    active = fields.Boolean(default=True)


class EducationInventoryItem(models.Model):
    _name = 'education.inventory.item'
    _description = 'Inventory Item'
    _inherit = ['mail.thread']

    name = fields.Char(string='Item Name', required=True, tracking=True)
    code = fields.Char(string='Code')
    category_id = fields.Many2one('education.inventory.category',
                                    string='Category')
    branch_id = fields.Many2one('education.branch', string='Branch')
    quantity = fields.Float(string='Quantity', compute='_compute_quantity',
                             store=True)
    unit = fields.Char(string='Unit', default='pcs')
    min_quantity = fields.Float(string='Min Quantity')
    unit_price = fields.Float(string='Unit Price')
    total_value = fields.Float(compute='_compute_total_value',
                                string='Total Value', store=True)
    location = fields.Char(string='Storage Location')
    active = fields.Boolean(default=True)

    movement_ids = fields.One2many('education.inventory.movement', 'item_id',
                                    string='Movements')

    @api.depends('movement_ids.quantity', 'movement_ids.movement_type')
    def _compute_quantity(self):
        for rec in self:
            incoming = sum(rec.movement_ids.filtered(
                lambda m: m.movement_type == 'in').mapped('quantity'))
            outgoing = sum(rec.movement_ids.filtered(
                lambda m: m.movement_type == 'out').mapped('quantity'))
            rec.quantity = incoming - outgoing

    @api.depends('quantity', 'unit_price')
    def _compute_total_value(self):
        for rec in self:
            rec.total_value = rec.quantity * rec.unit_price


class EducationInventoryMovement(models.Model):
    _name = 'education.inventory.movement'
    _description = 'Inventory Movement'
    _order = 'date desc'

    item_id = fields.Many2one('education.inventory.item', string='Item',
                               required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    movement_type = fields.Selection([
        ('in', 'Incoming'),
        ('out', 'Outgoing'),
    ], string='Type', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    unit_price = fields.Float(string='Unit Price')
    total_value = fields.Float(compute='_compute_total', string='Total Value',
                                store=True)
    reference = fields.Char(string='Reference')
    notes = fields.Text(string='Notes')
    user_id = fields.Many2one('res.users', string='Processed By',
                               default=lambda self: self.env.user)

    @api.depends('quantity', 'unit_price')
    def _compute_total(self):
        for rec in self:
            rec.total_value = rec.quantity * rec.unit_price


class EducationInventoryRequest(models.Model):
    _name = 'education.inventory.request'
    _description = 'Inventory Request'
    _order = 'date desc'

    name = fields.Char(string='Request Reference', readonly=True,
                       default=lambda self: _('New'))
    date = fields.Date(string='Date', default=fields.Date.today)
    requested_by = fields.Many2one('res.users', string='Requested By',
                                    default=lambda self: self.env.user)
    department_id = fields.Many2one('education.department', string='Department')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('fulfilled', 'Fulfilled'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')
    line_ids = fields.One2many('education.inventory.request.line', 'request_id',
                                string='Items')
    notes = fields.Text(string='Notes')


class EducationInventoryRequestLine(models.Model):
    _name = 'education.inventory.request.line'
    _description = 'Inventory Request Line'

    request_id = fields.Many2one('education.inventory.request',
                                  string='Request', required=True,
                                  ondelete='cascade')
    item_id = fields.Many2one('education.inventory.item', string='Item',
                               required=True)
    quantity = fields.Float(string='Requested Qty', required=True)
    approved_quantity = fields.Float(string='Approved Qty')
    notes = fields.Char(string='Notes')
