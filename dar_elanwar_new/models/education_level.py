from odoo import models, fields


class EducationLevel(models.Model):
    _name = 'education.level'
    _description = 'Education Level'

    name = fields.Char(string='Level Name', required=True)
    code = fields.Char(string='Code', required=True)
    department_id = fields.Many2one('education.department', string='Department',
                                     required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(default=True)

    class_ids = fields.One2many('education.class', 'level_id', string='Classes')

    _sql_constraints = [
        ('code_dept_uniq', 'unique(code, department_id)',
         'Level code must be unique per department!'),
    ]
