from odoo import models, fields


class EducationStudentArchive(models.Model):
    _name = 'education.student.archive'
    _description = 'Student Archive Record'
    _order = 'archive_date desc'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True, ondelete='cascade')
    archive_date = fields.Date(string='Archive Date', required=True,
                                default=fields.Date.today)
    reason_id = fields.Many2one('education.leave.reason', string='Reason')
    return_date = fields.Date(string='Return Date')
    notes = fields.Text(string='Notes')
