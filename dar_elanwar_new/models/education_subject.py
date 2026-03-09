from odoo import models, fields


class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'

    name = fields.Char(string='Subject Name', required=True)
    code = fields.Char(string='Code', required=True)
    department_id = fields.Many2one('education.department', string='Department',
                                     required=True, ondelete='cascade')
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Subject code must be unique!'),
    ]
