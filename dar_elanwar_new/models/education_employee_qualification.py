from odoo import models, fields


class EducationEmployeeQualification(models.Model):
    _name = 'education.employee.qualification'
    _description = 'Employee Qualification'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    name = fields.Char(string='Qualification', required=True)
    institution = fields.Char(string='Institution')
    date = fields.Date(string='Date')
    certificate = fields.Binary(string='Certificate', attachment=True)
