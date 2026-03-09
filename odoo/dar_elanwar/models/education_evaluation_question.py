# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationEvaluationQuestion(models.Model):
    _name = 'education.evaluation.question'
    _description = 'Evaluation Question'
    _order = 'template_id, sequence'

    template_id = fields.Many2one(
        'education.evaluation.template',
        string='Template',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    question = fields.Char(
        string='Question',
        required=True,
    )
    scale_id = fields.Many2one(
        'education.grade.scale',
        string='Grade Scale',
        required=True,
        help='The scale used to answer this question',
    )
    description = fields.Text(
        string='Description',
        help='Additional description or guidance for this question',
    )
    is_required = fields.Boolean(
        string='Required',
        default=True,
    )

    # Related
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        related='template_id.department_id',
        store=True,
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.sequence}. {record.question}"
            result.append((record.id, name))
        return result
