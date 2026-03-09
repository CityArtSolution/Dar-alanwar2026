from odoo import models, fields


class EducationGradeScale(models.Model):
    _name = 'education.grade.scale'
    _description = 'Grade Scale'

    name = fields.Char(string='Scale Name', required=True)
    code = fields.Char(string='Code')
    value_ids = fields.One2many('education.grade.scale.value', 'scale_id',
                                 string='Scale Values')
    active = fields.Boolean(default=True)


class EducationGradeScaleValue(models.Model):
    _name = 'education.grade.scale.value'
    _description = 'Grade Scale Value'
    _order = 'numeric_value desc'

    name = fields.Char(string='Grade Label', required=True)
    scale_id = fields.Many2one('education.grade.scale', string='Scale',
                                required=True, ondelete='cascade')
    numeric_value = fields.Float(string='Numeric Value')
