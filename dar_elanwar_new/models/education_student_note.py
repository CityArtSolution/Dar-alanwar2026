from odoo import models, fields


class EducationStudentNote(models.Model):
    _name = 'education.student.note'
    _description = 'Student Note'
    _order = 'date desc'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    note_type = fields.Selection([
        ('academic', 'Academic'),
        ('behavioral', 'Behavioral'),
        ('medical', 'Medical'),
        ('general', 'General'),
    ], string='Type', default='general')
    note = fields.Text(string='Note', required=True)
    is_important = fields.Boolean(string='Important')
    user_id = fields.Many2one('res.users', string='Created By',
                               default=lambda self: self.env.user)
