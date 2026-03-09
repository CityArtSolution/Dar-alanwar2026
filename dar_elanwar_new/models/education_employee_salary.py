from odoo import models, fields, api


SALARY_STATES = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('paid', 'Paid'),
    ('cancelled', 'Cancelled'),
]

MONTHS = [
    ('1', 'January'), ('2', 'February'), ('3', 'March'),
    ('4', 'April'), ('5', 'May'), ('6', 'June'),
    ('7', 'July'), ('8', 'August'), ('9', 'September'),
    ('10', 'October'), ('11', 'November'), ('12', 'December'),
]


class EducationEmployeeSalary(models.Model):
    _name = 'education.employee.salary'
    _description = 'Employee Salary'
    _order = 'year desc, month desc'

    employee_id = fields.Many2one('education.employee', string='Employee',
                                   required=True, ondelete='cascade')
    month = fields.Selection(MONTHS, string='Month', required=True)
    year = fields.Char(string='Year', required=True)
    basic_salary = fields.Float(string='Basic Salary')
    bonuses = fields.Float(string='Bonuses')
    deductions = fields.Float(string='Deductions')
    loan_deduction = fields.Float(string='Loan Deduction',
                                   compute='_compute_loan_deduction', store=True)
    net_salary = fields.Float(string='Net Salary',
                               compute='_compute_net_salary', store=True)
    state = fields.Selection(SALARY_STATES, string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.depends('employee_id', 'employee_id.loan_ids')
    def _compute_loan_deduction(self):
        for rec in self:
            active_loans = rec.employee_id.loan_ids.filtered(
                lambda l: l.status == 'active')
            rec.loan_deduction = sum(l.monthly_deduction for l in active_loans)

    @api.depends('basic_salary', 'bonuses', 'deductions', 'loan_deduction')
    def _compute_net_salary(self):
        for rec in self:
            rec.net_salary = (rec.basic_salary + rec.bonuses
                               - rec.deductions - rec.loan_deduction)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
