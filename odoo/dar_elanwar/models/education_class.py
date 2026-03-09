# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Education Class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'department_id, level_id, name'

    name = fields.Char(
        string='Class Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
        tracking=True,
    )
    level_id = fields.Many2one(
        'education.level',
        string='Level',
        domain="[('department_id', '=', department_id)]",
        tracking=True,
    )
    schedule_id = fields.Many2one(
        'education.schedule',
        string='Schedule',
        tracking=True,
    )
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
        domain="[('is_current', '=', True)]",
    )
    capacity = fields.Integer(
        string='Capacity',
        default=30,
    )
    teacher_id = fields.Many2one(
        'education.employee',
        string='Class Teacher',
    )
    room = fields.Char(
        string='Room',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    student_ids = fields.One2many(
        'res.partner',
        'class_id',
        string='Students',
        domain=[('is_student', '=', True)],
    )
    homework_ids = fields.One2many(
        'education.homework',
        'class_id',
        string='Homework',
    )
    attendance_ids = fields.One2many(
        'education.attendance',
        'class_id',
        string='Attendance Records',
    )

    # Computed
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_student_count',
    )
    available_seats = fields.Integer(
        string='Available Seats',
        compute='_compute_available_seats',
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
    subscription_count = fields.Integer(
        string='Subscriptions',
        compute='_compute_stat_counts',
    )
    total_fees = fields.Float(
        string='Total Fees',
        compute='_compute_stat_counts',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Class code must be unique!'),
    ]

    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids.filtered(lambda s: s.student_state == 'enrolled'))

    @api.depends('capacity', 'student_count')
    def _compute_available_seats(self):
        for record in self:
            record.available_seats = record.capacity - record.student_count

    @api.depends('homework_ids', 'attendance_ids', 'student_ids')
    def _compute_stat_counts(self):
        for record in self:
            record.homework_count = len(record.homework_ids)
            record.attendance_count = len(record.attendance_ids)
            # Evaluations for students in this class
            record.evaluation_count = self.env['education.student.evaluation'].search_count([
                ('student_id', 'in', record.student_ids.ids)
            ])
            # Subscriptions for students in this class
            subscriptions = self.env['education.student.subscription'].search([
                ('student_id', 'in', record.student_ids.ids)
            ])
            record.subscription_count = len(subscriptions)
            record.total_fees = sum(subscriptions.mapped('total_amount'))

    # Stat button actions
    def action_view_students(self):
        """View class students"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('is_student', '=', True), ('class_id', '=', self.id)],
            'context': {'default_class_id': self.id, 'default_department_id': self.department_id.id, 'default_is_student': True},
        }

    def action_view_homework(self):
        """View class homework"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'education.homework',
            'view_mode': 'list,form',
            'domain': [('class_id', '=', self.id)],
            'context': {'default_class_id': self.id},
        }

    def action_view_attendance(self):
        """View class attendance"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'education.attendance',
            'view_mode': 'list,form',
            'domain': [('class_id', '=', self.id)],
            'context': {'default_class_id': self.id, 'default_department_id': self.department_id.id},
        }

    def action_view_evaluations(self):
        """View evaluations for students in this class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations',
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', self.student_ids.ids)],
        }

    def action_view_subscriptions(self):
        """View subscriptions for students in this class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', self.student_ids.ids)],
        }

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Clear level when department changes"""
        if self.department_id:
            if self.level_id and self.level_id.department_id != self.department_id:
                self.level_id = False
        else:
            self.level_id = False

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.department_id:
                name = f"{record.department_id.name} / {record.name}"
            result.append((record.id, name))
        return result
