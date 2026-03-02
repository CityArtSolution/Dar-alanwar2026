# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationStudentEvaluation(models.Model):
    _name = 'education.student.evaluation'
    _description = 'Student Evaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'goal_id, student_id'

    goal_id = fields.Many2one(
        'education.evaluation.goal',
        string='Evaluation Goal',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
    )
    evaluator_id = fields.Many2one(
        'education.employee',
        string='Evaluator',
        required=True,
    )
    date = fields.Date(
        string='Evaluation Date',
        required=True,
        default=fields.Date.context_today,
    )
    summary = fields.Text(
        string='Summary',
        help='Overall summary of the student evaluation',
    )
    is_completed = fields.Boolean(
        string='Completed',
        default=False,
        tracking=True,
    )
    completed_date = fields.Date(
        string='Completed Date',
    )

    # Related fields
    template_id = fields.Many2one(
        'education.evaluation.template',
        string='Template',
        related='goal_id.template_id',
        store=True,
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        related='goal_id.class_id',
        store=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        related='goal_id.department_id',
        store=True,
    )

    # Answer lines
    answer_ids = fields.One2many(
        'education.evaluation.answer',
        'evaluation_id',
        string='Answers',
    )

    # Computed
    answer_count = fields.Integer(
        string='Answer Count',
        compute='_compute_answer_count',
    )
    question_count = fields.Integer(
        string='Question Count',
        compute='_compute_answer_count',
    )
    completion_rate = fields.Float(
        string='Completion Rate',
        compute='_compute_answer_count',
    )

    @api.depends('answer_ids', 'goal_id.template_id.question_ids')
    def _compute_answer_count(self):
        for record in self:
            record.answer_count = len(record.answer_ids)
            record.question_count = len(record.goal_id.template_id.question_ids)
            if record.question_count:
                record.completion_rate = (record.answer_count / record.question_count) * 100
            else:
                record.completion_rate = 0.0

    def action_complete(self):
        """Mark the evaluation as completed"""
        self.write({
            'is_completed': True,
            'completed_date': fields.Date.today(),
        })

    def action_reset(self):
        """Reset to incomplete"""
        self.write({
            'is_completed': False,
            'completed_date': False,
        })

    def action_load_questions(self):
        """Load all template questions as empty answers"""
        for record in self:
            existing_question_ids = record.answer_ids.mapped('question_id').ids
            for question in record.goal_id.template_id.question_ids:
                if question.id not in existing_question_ids:
                    self.env['education.evaluation.answer'].create({
                        'evaluation_id': record.id,
                        'question_id': question.id,
                    })

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.student_id.name} - {record.goal_id.name}"
            result.append((record.id, name))
        return result
