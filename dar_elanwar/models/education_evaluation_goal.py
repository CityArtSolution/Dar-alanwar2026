# -*- coding: utf-8 -*-

from odoo import models, fields, api

GOAL_STATES = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class EducationEvaluationGoal(models.Model):
    _name = 'education.evaluation.goal'
    _description = 'Evaluation Goal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, name'

    name = fields.Char(
        string='Goal Name',
        required=True,
        tracking=True,
    )
    date = fields.Date(
        string='Evaluation Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    template_id = fields.Many2one(
        'education.evaluation.template',
        string='Evaluation Template',
        required=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        related='template_id.department_id',
        store=True,
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        required=True,
        domain="[('department_id', '=', department_id)]",
    )
    teacher_id = fields.Many2one(
        'education.employee',
        string='Evaluator',
        required=True,
        domain="[('is_teacher', '=', True)]",
    )
    description = fields.Text(
        string='Description',
    )
    is_shared = fields.Boolean(
        string='Shared with Parents',
        default=False,
        help='If checked, evaluation results will be visible to parents',
    )
    state = fields.Selection(
        selection=GOAL_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related evaluations
    evaluation_ids = fields.One2many(
        'education.student.evaluation',
        'goal_id',
        string='Student Evaluations',
    )

    # Computed
    evaluation_count = fields.Integer(
        string='Evaluation Count',
        compute='_compute_evaluation_count',
    )
    completed_count = fields.Integer(
        string='Completed Count',
        compute='_compute_evaluation_count',
    )
    progress = fields.Float(
        string='Progress',
        compute='_compute_evaluation_count',
    )

    @api.depends('evaluation_ids', 'evaluation_ids.is_completed')
    def _compute_evaluation_count(self):
        for record in self:
            record.evaluation_count = len(record.evaluation_ids)
            record.completed_count = len(record.evaluation_ids.filtered('is_completed'))
            if record.evaluation_count:
                record.progress = (record.completed_count / record.evaluation_count) * 100
            else:
                record.progress = 0.0

    def action_activate(self):
        """Activate the evaluation goal and create student evaluations"""
        for record in self:
            # Get all enrolled students in the class
            students = self.env['res.partner'].search([
                ('is_student', '=', True),
                ('class_id', '=', record.class_id.id),
                ('student_state', '=', 'enrolled'),
            ])
            # Create evaluation records for each student
            for student in students:
                self.env['education.student.evaluation'].create({
                    'goal_id': record.id,
                    'student_id': student.id,
                    'evaluator_id': record.teacher_id.id,
                    'date': record.date,
                })
            record.state = 'active'

    def action_complete(self):
        """Mark the evaluation goal as completed"""
        self.write({'state': 'completed'})

    def action_cancel(self):
        """Cancel the evaluation goal"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
