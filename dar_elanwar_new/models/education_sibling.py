from odoo import models, fields


class EducationSibling(models.Model):
    _name = 'education.sibling'
    _description = 'Student Sibling'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True, ondelete='cascade')
    name = fields.Char(string='Sibling Name', required=True)
    birthdate = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    is_enrolled = fields.Boolean(string='Is Enrolled')
    enrolled_student_id = fields.Many2one('education.student',
                                           string='Enrolled As')
