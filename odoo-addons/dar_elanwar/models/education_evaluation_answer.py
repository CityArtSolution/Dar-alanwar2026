# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationEvaluationAnswer(models.Model):
    _name = 'education.evaluation.answer'
    _description = 'Evaluation Answer'
    _order = 'evaluation_id, question_id'

    evaluation_id = fields.Many2one(
        'education.student.evaluation',
        string='Student Evaluation',
        required=True,
        ondelete='cascade',
    )
    question_id = fields.Many2one(
        'education.evaluation.question',
        string='Question',
        required=True,
    )
    answer_value_id = fields.Many2one(
        'education.grade.scale.value',
        string='Answer',
        domain="[('scale_id', '=', scale_id)]",
    )
    notes = fields.Char(
        string='Notes',
    )

    # Related fields
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        related='evaluation_id.student_id',
        store=True,
    )
    scale_id = fields.Many2one(
        'education.grade.scale',
        string='Grade Scale',
        related='question_id.scale_id',
        store=True,
    )
    question_text = fields.Char(
        string='Question Text',
        related='question_id.question',
    )
    sequence = fields.Integer(
        string='Sequence',
        related='question_id.sequence',
        store=True,
    )

    # Numeric value for calculations
    numeric_value = fields.Float(
        string='Numeric Value',
        related='answer_value_id.numeric_value',
        store=True,
    )

    _sql_constraints = [
        ('evaluation_question_unique', 'UNIQUE(evaluation_id, question_id)',
         'Each question can only have one answer per evaluation!'),
    ]
