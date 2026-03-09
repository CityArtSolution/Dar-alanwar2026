from odoo import models, fields, api


class EducationHomework(models.Model):
    _name = 'education.homework'
    _description = 'Homework Assignment'
    _inherit = ['mail.thread']
    _order = 'due_date desc'

    name = fields.Char(string='Title', required=True, tracking=True)
    description = fields.Html(string='Description')
    class_id = fields.Many2one('education.class', string='Class', required=True)
    subject_id = fields.Many2one('education.subject', string='Subject')
    teacher_id = fields.Many2one('education.employee', string='Teacher',
                                  domain=[('is_teacher', '=', True)])
    assign_date = fields.Date(string='Assigned Date',
                               default=fields.Date.today)
    due_date = fields.Date(string='Due Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    attachment = fields.Binary(string='Attachment', attachment=True)
    attachment_name = fields.Char(string='Attachment Name')

    submission_ids = fields.One2many('education.homework.submission',
                                      'homework_id', string='Submissions')
    submission_count = fields.Integer(compute='_compute_submission_count',
                                       string='Submissions')

    def _compute_submission_count(self):
        for rec in self:
            rec.submission_count = len(rec.submission_ids)

    def action_publish(self):
        self.write({'state': 'published'})

    def action_close(self):
        self.write({'state': 'closed'})


class EducationHomeworkSubmission(models.Model):
    _name = 'education.homework.submission'
    _description = 'Homework Submission'
    _order = 'submit_date desc'

    homework_id = fields.Many2one('education.homework', string='Homework',
                                   required=True, ondelete='cascade')
    student_id = fields.Many2one('education.student', string='Student',
                                  required=True)
    submit_date = fields.Datetime(string='Submitted At',
                                    default=fields.Datetime.now)
    content = fields.Text(string='Answer')
    attachment = fields.Binary(string='Attachment', attachment=True)
    attachment_name = fields.Char(string='Attachment Name')
    grade = fields.Float(string='Grade')
    feedback = fields.Text(string='Teacher Feedback')
    is_graded = fields.Boolean(string='Graded', default=False)
