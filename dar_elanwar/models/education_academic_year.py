# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EducationAcademicYear(models.Model):
    _name = 'education.academic.year'
    _description = 'Academic Year'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(
        string='Academic Year',
        required=True,
        tracking=True,
        help='e.g., 2024-2025',
    )
    date_start = fields.Date(
        string='Start Date',
        required=True,
        tracking=True,
    )
    date_end = fields.Date(
        string='End Date',
        required=True,
        tracking=True,
    )
    is_current = fields.Boolean(
        string='Current Year',
        default=False,
        tracking=True,
        help='Check if this is the current academic year',
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

    _name_unique = models.Constraint(
        'UNIQUE(name, company_id)',
        'Academic year name must be unique per company!',
    )

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Ensure end date is after start date"""
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end <= record.date_start:
                    raise ValidationError('End date must be after start date!')

    @api.constrains('is_current')
    def _check_current_year(self):
        """Ensure only one current academic year exists"""
        for record in self:
            if record.is_current:
                existing_current = self.search([
                    ('is_current', '=', True),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id),
                ])
                if existing_current:
                    existing_current.write({'is_current': False})

    def action_set_current(self):
        """Set this academic year as current"""
        self.ensure_one()
        self.search([
            ('is_current', '=', True),
            ('company_id', '=', self.company_id.id),
        ]).write({'is_current': False})
        self.write({'is_current': True})

    # Related records
    class_ids = fields.One2many(
        'education.class',
        'academic_year_id',
        string='Classes',
    )
    student_ids = fields.One2many(
        'res.partner',
        'academic_year_id',
        string='Students',
    )

    # Computed counts for stat buttons
    student_count = fields.Integer(
        string='Students',
        compute='_compute_stat_counts',
    )
    subscription_count = fields.Integer(
        string='Subscriptions',
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
    attendance_count = fields.Integer(
        string='Attendance',
        compute='_compute_stat_counts',
    )
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_stat_counts',
    )

    def _compute_stat_counts(self):
        for record in self:
            record.class_count = len(record.class_ids)
            record.student_count = len(record.student_ids)
            record.subscription_count = self.env['education.student.subscription'].search_count([
                ('start_date', '>=', record.date_start),
                ('start_date', '<=', record.date_end),
            ])
            # Count homework for classes in this academic year
            class_ids = record.class_ids.ids
            record.homework_count = self.env['education.homework'].search_count([
                ('class_id', 'in', class_ids),
            ]) if class_ids else 0
            # Count attendance for this academic year
            record.attendance_count = self.env['education.attendance'].search_count([
                ('date', '>=', record.date_start),
                ('date', '<=', record.date_end),
            ])
            # Count evaluations for this academic year
            record.evaluation_count = self.env['education.evaluation.goal'].search_count([
                ('date', '>=', record.date_start),
                ('date', '<=', record.date_end),
            ])

    # Stat button actions
    def action_view_students(self):
        """View students enrolled this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [
                ('enrollment_date', '>=', self.date_start),
                ('enrollment_date', '<=', self.date_end),
            ],
        }

    def action_view_subscriptions(self):
        """View subscriptions for this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [
                ('start_date', '>=', self.date_start),
                ('start_date', '<=', self.date_end),
            ],
        }

    def action_view_classes(self):
        """View classes for this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Classes',
            'res_model': 'education.class',
            'view_mode': 'list,form',
            'domain': [('academic_year_id', '=', self.id)],
            'context': {'default_academic_year_id': self.id},
        }

    def action_view_homework(self):
        """View homework for this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'education.homework',
            'view_mode': 'list,form',
            'domain': [('class_id', 'in', self.class_ids.ids)],
        }

    def action_view_attendance(self):
        """View attendance for this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'education.attendance',
            'view_mode': 'list,form',
            'domain': [
                ('date', '>=', self.date_start),
                ('date', '<=', self.date_end),
            ],
        }

    def action_view_evaluations(self):
        """View evaluations for this academic year"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluation Goals',
            'res_model': 'education.evaluation.goal',
            'view_mode': 'list,kanban,form',
            'domain': [
                ('date', '>=', self.date_start),
                ('date', '<=', self.date_end),
            ],
        }
