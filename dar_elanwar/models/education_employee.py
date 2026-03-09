# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date

GENDER_TYPES = [
    ('male', 'Male / ذكر'),
    ('female', 'Female / أنثى'),
]

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
    _order = 'name'

    # Basic Information
    code = fields.Char(
        string='Employee Code',
        readonly=True,
        copy=False,
        default='New',
    )
    name = fields.Char(
        string='Full Name',
        required=True,
        tracking=True,
    )
    photo = fields.Binary(
        string='Photo',
        attachment=True,
    )
    phone = fields.Char(
        string='Phone',
    )
    mobile = fields.Char(
        string='Mobile',
    )
    email = fields.Char(
        string='Email',
    )
    birthdate = fields.Date(
        string='Birth Date',
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    gender = fields.Selection(
        selection=GENDER_TYPES,
        string='Gender',
        default='male',
    )
    id_number = fields.Char(
        string='ID Number',
    )
    address = fields.Text(
        string='Address',
    )

    # Job Information
    category_id = fields.Many2one(
        'education.employee.category',
        string='Category',
        tracking=True,
    )
    job_title = fields.Char(
        string='Job Title',
        tracking=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
    )
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
    )
    hire_date = fields.Date(
        string='Hire Date',
        tracking=True,
    )
    end_date = fields.Date(
        string='End Date',
    )
    is_teacher = fields.Boolean(
        string='Is Teacher',
        default=False,
    )

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
        string='Assigned Classes',
    )

    # Salary
    salary = fields.Float(
        string='Basic Salary',
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )

    # Qualification
    qualification = fields.Char(
        string='Qualification',
    )

    # State
    state = fields.Selection(
        selection=EMPLOYEE_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # User link
    user_id = fields.Many2one(
        'res.users',
        string='Related User',
    )

    # Related records
    qualification_ids = fields.One2many(
        'education.employee.qualification',
        'employee_id',
        string='Qualifications',
    )
    attendance_ids = fields.One2many(
        'education.employee.attendance',
        'employee_id',
        string='Attendance',
    )
    salary_ids = fields.One2many(
        'education.employee.salary',
        'employee_id',
        string='Salaries',
    )
    penalty_ids = fields.One2many(
        'education.employee.penalty',
        'employee_id',
        string='Penalties',
    )
    complaint_ids = fields.One2many(
        'education.employee.complaint',
        'employee_id',
        string='Complaints',
    )
    loan_ids = fields.One2many(
        'education.employee.loan',
        'employee_id',
        string='Loans',
    )
    class_ids = fields.One2many(
        'education.class',
        'teacher_id',
        string='Classes',
    )
    homework_ids = fields.One2many(
        'education.homework',
        'teacher_id',
        string='Homework Assigned',
    )
    evaluation_ids = fields.One2many(
        'education.student.evaluation',
        'evaluator_id',
        string='Evaluations Done',
    )
    # Computed counts for stat buttons
    attendance_count = fields.Integer(
        string='Attendance',
        compute='_compute_stat_counts',
    )
    salary_count = fields.Integer(
        string='Salaries',
        compute='_compute_stat_counts',
    )
    penalty_count = fields.Integer(
        string='Penalties',
        compute='_compute_stat_counts',
    )
    complaint_count = fields.Integer(
        string='Complaints',
        compute='_compute_stat_counts',
    )
    loan_count = fields.Integer(
        string='Loans',
        compute='_compute_stat_counts',
    )
    class_count = fields.Integer(
        string='Classes',
        compute='_compute_stat_counts',
    )
    homework_count = fields.Integer(
        string='Homework',
        compute='_compute_stat_counts',
    )
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_stat_counts',
    )
    _code_unique = models.Constraint(
        'UNIQUE(code)',
        'Employee code must be unique!',
    )

    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birthdate:
                delta = relativedelta(today, record.birthdate)
                record.age = delta.years
            else:
                record.age = 0

    def _compute_stat_counts(self):
        for record in self:
            record.attendance_count = len(record.attendance_ids)
            record.salary_count = len(record.salary_ids)
            record.penalty_count = len(record.penalty_ids)
            record.complaint_count = len(record.complaint_ids)
            record.loan_count = len(record.loan_ids)
            record.class_count = len(record.class_ids)
            record.homework_count = len(record.homework_ids)
            record.evaluation_count = len(record.evaluation_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'New') == 'New':
                vals['code'] = self.env['ir.sequence'].next_by_code('education.employee') or 'New'
        return super().create(vals_list)

    def action_activate(self):
        """Activate the employee"""
        self.write({'state': 'active'})

    def action_on_leave(self):
        """Set employee on leave"""
        self.write({'state': 'on_leave'})

    def action_terminate(self):
        """Terminate the employee"""
        self.write({'state': 'terminated', 'end_date': fields.Date.today()})

    def action_reactivate(self):
        """Reactivate terminated employee"""
        self.write({'state': 'active', 'end_date': False})

    # Stat button actions
    def action_view_attendance(self):
        """View employee attendance"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'education.employee.attendance',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_salaries(self):
        """View employee salaries"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Salaries',
            'res_model': 'education.employee.salary',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_penalties(self):
        """View employee penalties"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Penalties',
            'res_model': 'education.employee.penalty',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_complaints(self):
        """View employee complaints"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Complaints',
            'res_model': 'education.employee.complaint',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_loans(self):
        """View employee loans"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Loans',
            'res_model': 'education.employee.loan',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_classes(self):
        """View classes taught by employee"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Classes',
            'res_model': 'education.class',
            'view_mode': 'list,form',
            'domain': [('teacher_id', '=', self.id)],
            'context': {'default_teacher_id': self.id},
        }

    def action_view_homework(self):
        """View homework assigned by employee"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'education.homework',
            'view_mode': 'list,form',
            'domain': [('teacher_id', '=', self.id)],
            'context': {'default_teacher_id': self.id},
        }

    def action_view_evaluations(self):
        """View evaluations done by employee"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations',
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('evaluator_id', '=', self.id)],
            'context': {'default_evaluator_id': self.id},
        }

