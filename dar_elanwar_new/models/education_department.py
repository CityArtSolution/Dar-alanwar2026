from odoo import models, fields


DEPARTMENT_TYPES = [
    ('kindergarten', 'Kindergarten'),
    ('primary', 'Primary'),
    ('intermediate', 'Intermediate'),
    ('secondary', 'Secondary'),
    ('quran', 'Quran Memorization'),
    ('special', 'Special Education'),
    ('other', 'Other'),
]


class EducationDepartment(models.Model):
    _name = 'education.department'
    _description = 'Education Department'
    _inherit = ['mail.thread']

    name = fields.Char(string='Department Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True)
    type = fields.Selection(DEPARTMENT_TYPES, string='Type', required=True)
    branch_id = fields.Many2one('education.branch', string='Branch', required=True)
    active = fields.Boolean(default=True)

    level_ids = fields.One2many('education.level', 'department_id', string='Levels')
    class_ids = fields.One2many('education.class', 'department_id', string='Classes')
    subject_ids = fields.One2many('education.subject', 'department_id', string='Subjects')

    student_count = fields.Integer(compute='_compute_student_count', string='Students')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Department code must be unique!'),
    ]

    def _compute_student_count(self):
        for rec in self:
            rec.student_count = self.env['education.student'].search_count(
                [('department_id', '=', rec.id)])
