from odoo import models, fields


class EducationEnrollmentSource(models.Model):
    _name = 'education.enrollment.source'
    _description = 'Enrollment Source'

    name = fields.Char(string='Source Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)
