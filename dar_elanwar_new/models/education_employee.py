from odoo import models, fields, api, _


EMPLOYEE_STATES = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('on_leave', 'On Leave'),
    ('terminated', 'Terminated'),
]


class EducationEmployee(models.Model):
    _name = 'education.employee'
    _description = 'Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code'

    code = fields.Char(string='Employee Code', readonly=True, copy=False,
                       default=lambda self: _('New'))
    name = fields.Char(string='Full Name', required=True, tracking=True)
    arabic_name = fields.Char(string='Name (Arabic)')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    birthdate = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    id_number = fields.Char(string='National ID')
    photo = fields.Binary(string='Photo', attachment=True)

    category_id = fields.Many2one('education.employee.category',
                                    string='Category')
    job_title = fields.Char(string='Job Title')
    department_id = fields.Many2one('education.department', string='Department')
    branch_id = fields.Many2one('education.branch', string='Branch')
    hire_date = fields.Date(string='Hire Date')
    is_teacher = fields.Boolean(string='Is Teacher', default=False)

    # PRD Gap Fields
    shift_type = fields.Selection([
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
    ], string='Shift Type', default='full_time')
    assigned_class_ids = fields.Many2many(
        'education.class',
        'education_employee_class_rel',
        'employee_id', 'class_id',
        string='Assigned Classes')

    salary = fields.Float(string='Basic Salary')
    state = fields.Selection(EMPLOYEE_STATES, string='Status', default='draft',
                              tracking=True)
    active = fields.Boolean(default=True)

    # Related Records
    class_ids = fields.One2many('education.class', 'teacher_id',
                                 string='Classes (Teacher)')
    qualification_ids = fields.One2many('education.employee.qualification',
                                         'employee_id', string='Qualifications')
    attendance_ids = fields.One2many('education.employee.attendance',
                                      'employee_id', string='Attendance')
    salary_ids = fields.One2many('education.employee.salary', 'employee_id',
                                  string='Salary Records')
    penalty_ids = fields.One2many('education.employee.penalty', 'employee_id',
                                   string='Penalties')
    complaint_ids = fields.One2many('education.employee.complaint',
                                     'employee_id', string='Complaints')
    loan_ids = fields.One2many('education.employee.loan', 'employee_id',
                                string='Loans')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Employee code must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'education.employee') or _('New')
        return super().create(vals_list)

    def action_activate(self):
        self.write({'state': 'active'})

    def action_set_on_leave(self):
        self.write({'state': 'on_leave'})

    def action_terminate(self):
        self.write({'state': 'terminated'})
