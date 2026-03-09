from odoo import models, fields


class EducationDiscount(models.Model):
    _name = 'education.discount'
    _description = 'Discount'

    name = fields.Char(string='Discount Name', required=True)
    discount_type = fields.Selection([
        ('sibling', 'Sibling Discount'),
        ('early_payment', 'Early Payment'),
        ('scholarship', 'Scholarship'),
        ('custom', 'Custom'),
    ], string='Discount Type', required=True)
    value_type = fields.Selection([
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Value Type', required=True, default='percentage')
    value = fields.Float(string='Value', required=True)
    department_id = fields.Many2one('education.department',
                                     string='Department')
    active = fields.Boolean(default=True)
    auto_apply = fields.Boolean(string='Auto Apply', default=False)
    min_siblings = fields.Integer(string='Min Siblings (for sibling discount)')
    early_days = fields.Integer(string='Days Before Due (for early payment)')
    description = fields.Text(string='Description')
