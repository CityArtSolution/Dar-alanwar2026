from odoo import models, fields


class EducationEmployeeComplaint(models.Model):
    _name = 'education.employee.complaint'
    _description = 'Employee Complaint'
    _order = 'date desc'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    complaint = fields.Text(string='Complaint', required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='new')
    resolution = fields.Text(string='Resolution')
