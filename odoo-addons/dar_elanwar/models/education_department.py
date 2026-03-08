# -*- coding: utf-8 -*-

from odoo import models, fields, api

DEPARTMENT_TYPES = [
    ('nursery', 'Nursery / حضانة'),
    ('quran', 'Quran / قرآن'),
    ('tutoring', 'Tutoring Groups / مجموعات تقوية'),
    ('literacy', 'Literacy / تعليم هجاء'),
    ('foundation', 'Foundation / مجموعات تأسيس'),
    ('courses', 'Courses / دورات'),
    ('summer', 'Summer Activities / نشاط صيفي'),
]


class EducationDepartment(models.Model):
    _name = 'education.department'
    _description = 'Education Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(
        string='Department Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
        tracking=True,
    )
    type = fields.Selection(
        selection=DEPARTMENT_TYPES,
        string='Type',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
    )

    # Related records
    level_ids = fields.One2many(
        'education.level',
        'department_id',
        string='Levels',
    )
    subject_ids = fields.One2many(
        'education.subject',
        'department_id',
        string='Subjects',
    )
    class_ids = fields.One2many(
        'education.class',
        'department_id',
        string='Classes',
    )

    # Computed fields
    level_count = fields.Integer(
        string='Level Count',
        compute='_compute_counts',
    )
    class_count = fields.Integer(
        string='Class Count',
        compute='_compute_counts',
    )
    subject_count = fields.Integer(
        string='Subject Count',
        compute='_compute_counts',
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_counts',
    )
    employee_count = fields.Integer(
        string='Employee Count',
        compute='_compute_counts',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Department code must be unique!'),
    ]

    @api.depends('level_ids', 'class_ids', 'subject_ids')
    def _compute_counts(self):
        for record in self:
            record.level_count = len(record.level_ids)
            record.class_count = len(record.class_ids)
            record.subject_count = len(record.subject_ids)
            record.student_count = self.env['res.partner'].search_count([
                ('is_student', '=', True),
                ('department_id', '=', record.id),
            ])
            record.employee_count = self.env['education.employee'].search_count([
                ('department_id', '=', record.id)
            ])

    # Stat button actions
    def action_view_levels(self):
        """View department levels"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Levels',
            'res_model': 'education.level',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_view_classes(self):
        """View department classes"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Classes',
            'res_model': 'education.class',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_view_subjects(self):
        """View department subjects"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subjects',
            'res_model': 'education.subject',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_view_students(self):
        """View department students"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('is_student', '=', True), ('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }

    def action_view_employees(self):
        """View department employees"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employees',
            'res_model': 'education.employee',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
        }
