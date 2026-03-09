from odoo import models, fields, api, _


MONTHS = [
    ('1', 'January'), ('2', 'February'), ('3', 'March'),
    ('4', 'April'), ('5', 'May'), ('6', 'June'),
    ('7', 'July'), ('8', 'August'), ('9', 'September'),
    ('10', 'October'), ('11', 'November'), ('12', 'December'),
]


class BatchPayrollWizard(models.TransientModel):
    _name = 'education.batch.payroll.wizard'
    _description = 'Batch Payroll Generation Wizard'

    month = fields.Selection(MONTHS, string='Month', required=True)
    year = fields.Char(string='Year', required=True,
                       default=lambda self: str(fields.Date.today().year))
    branch_id = fields.Many2one('education.branch', string='Branch')
    department_id = fields.Many2one('education.department', string='Department')
    employee_ids = fields.Many2many(
        'education.employee',
        'batch_payroll_employee_rel',
        'wizard_id', 'employee_id',
        string='Employees')

    @api.onchange('branch_id', 'department_id')
    def _onchange_filters(self):
        domain = [('state', '=', 'active')]
        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))
        self.employee_ids = self.env['education.employee'].search(domain)

    def action_generate_payroll(self):
        """Bulk create salary records for selected employees."""
        self.ensure_one()
        Salary = self.env['education.employee.salary']
        created = self.env['education.employee.salary']

        employees = self.employee_ids or self.env['education.employee'].search(
            [('state', '=', 'active')])

        for emp in employees:
            existing = Salary.search([
                ('employee_id', '=', emp.id),
                ('month', '=', self.month),
                ('year', '=', self.year),
            ], limit=1)
            if not existing:
                rec = Salary.create({
                    'employee_id': emp.id,
                    'month': self.month,
                    'year': self.year,
                    'basic_salary': emp.salary,
                })
                created |= rec

        return {
            'type': 'ir.actions.act_window',
            'name': _('Generated Salary Records'),
            'res_model': 'education.employee.salary',
            'view_mode': 'list,form',
            'domain': [('id', 'in', created.ids)],
        }
