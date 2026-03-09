# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationBranch(models.Model):
    _name = 'education.branch'
    _description = 'Education Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(
        string='Branch Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
        tracking=True,
    )
    address = fields.Text(
        string='Address',
    )
    phone = fields.Char(
        string='Phone',
    )
    email = fields.Char(
        string='Email',
    )
    is_main = fields.Boolean(
        string='Main Branch',
        default=False,
        help='Check if this is the main branch',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    # Related records
    department_ids = fields.One2many(
        'education.department',
        'branch_id',
        string='Departments',
    )
    student_ids = fields.One2many(
        'res.partner',
        'branch_id',
        string='Students',
    )
    employee_ids = fields.One2many(
        'education.employee',
        'branch_id',
        string='Employees',
    )

    # Computed counts
    department_count = fields.Integer(
        string='Departments',
        compute='_compute_counts',
    )
    student_count = fields.Integer(
        string='Students',
        compute='_compute_counts',
    )
    employee_count = fields.Integer(
        string='Employees',
        compute='_compute_counts',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Branch code must be unique!'),
    ]

    def _compute_counts(self):
        for record in self:
            record.department_count = len(record.department_ids)
            record.student_count = len(record.student_ids)
            record.employee_count = len(record.employee_ids)

    # Stat button actions
    def action_view_departments(self):
        """View branch departments"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Departments',
            'res_model': 'education.department',
            'view_mode': 'list,form',
            'domain': [('branch_id', '=', self.id)],
            'context': {'default_branch_id': self.id},
        }

    def action_view_students(self):
        """View branch students"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('branch_id', '=', self.id)],
            'context': {'default_branch_id': self.id},
        }

    def action_view_employees(self):
        """View branch employees"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employees',
            'res_model': 'education.employee',
            'view_mode': 'list,form',
            'domain': [('branch_id', '=', self.id)],
            'context': {'default_branch_id': self.id},
        }

    @api.constrains('is_main')
    def _check_main_branch(self):
        """Ensure only one main branch exists"""
        for record in self:
            if record.is_main:
                existing_main = self.search([
                    ('is_main', '=', True),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                ])
                if existing_main:
                    existing_main.write({'is_main': False})
