from odoo import models, fields


class EducationSchedule(models.Model):
    _name = 'education.schedule'
    _description = 'Class Schedule'

    name = fields.Char(string='Schedule Name', required=True)
    time_from = fields.Float(string='From')
    time_to = fields.Float(string='To')
    period = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    ], string='Period', default='morning')
    active = fields.Boolean(default=True)
