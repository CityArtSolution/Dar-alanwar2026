from odoo import models, fields, api


class EducationBranch(models.Model):
    _name = 'education.branch'
    _description = 'Education Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Branch Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    is_main = fields.Boolean(string='Main Branch', default=False)
    company_id = fields.Many2one('res.company', string='Company',
                                  default=lambda self: self.env.company)
    active = fields.Boolean(default=True)

    student_count = fields.Integer(compute='_compute_student_count', string='Students')
    employee_count = fields.Integer(compute='_compute_employee_count', string='Employees')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Branch code must be unique!'),
    ]

    def _compute_student_count(self):
        for rec in self:
            rec.student_count = self.env['education.student'].search_count(
                [('branch_id', '=', rec.id)])

    def _compute_employee_count(self):
        for rec in self:
            rec.employee_count = self.env['education.employee'].search_count(
                [('branch_id', '=', rec.id)])
