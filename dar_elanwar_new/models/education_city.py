from odoo import models, fields


class EducationCity(models.Model):
    _name = 'education.city'
    _description = 'City'

    name = fields.Char(string='City Name', required=True)
    code = fields.Char(string='Code')
    country_id = fields.Many2one('res.country', string='Country')
    active = fields.Boolean(default=True)
