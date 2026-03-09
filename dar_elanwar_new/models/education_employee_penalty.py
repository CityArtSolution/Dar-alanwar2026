from odoo import models, fields


class EducationEmployeePenalty(models.Model):
    _name = 'education.employee.penalty'
    _description = 'Employee Penalty'
    _order = 'date desc'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    reason = fields.Text(string='Reason', required=True)
    penalty_type = fields.Selection([
        ('warning', 'Warning'),
        ('fine', 'Fine'),
        ('suspension', 'Suspension'),
        ('termination', 'Termination'),
    ], string='Penalty Type', required=True)
    amount = fields.Float(string='Fine Amount')
    notes = fields.Text(string='Notes')
