from odoo import models, fields


class EducationEmployeeCategory(models.Model):
    _name = 'education.employee.category'
    _description = 'Employee Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)
