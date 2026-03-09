from odoo import models, fields


class EducationReminder(models.Model):
    _name = 'education.reminder'
    _description = 'Reminder'
    _order = 'date asc, time asc'

    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    date = fields.Date(string='Date', required=True)
    time = fields.Float(string='Time')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='medium')
    is_done = fields.Boolean(string='Done', default=False)
    user_id = fields.Many2one('res.users', string='Assigned To',
                               default=lambda self: self.env.user)
