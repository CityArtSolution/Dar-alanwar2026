# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationEvaluationTemplate(models.Model):
    _name = 'education.evaluation.template'
    _description = 'Evaluation Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Template Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
    )
    subject_id = fields.Many2one(
        'education.subject',
        string='Subject',
        domain="[('department_id', '=', department_id)]",
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related questions
    question_ids = fields.One2many(
        'education.evaluation.question',
        'template_id',
        string='Questions',
    )

    # Computed
    question_count = fields.Integer(
        string='Question Count',
        compute='_compute_question_count',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Template code must be unique!'),
    ]

    @api.depends('question_ids')
    def _compute_question_count(self):
        for record in self:
            record.question_count = len(record.question_ids)

    # Computed counts for stat buttons
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_evaluation_count',
    )

    def _compute_evaluation_count(self):
        for record in self:
            record.evaluation_count = self.env['education.student.evaluation'].search_count([
                ('template_id', '=', record.id)
            ])

    # Stat button actions
    def action_view_questions(self):
        """View template questions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questions',
            'res_model': 'education.evaluation.question',
            'view_mode': 'list,form',
            'domain': [('template_id', '=', self.id)],
            'context': {'default_template_id': self.id},
        }

    def action_view_evaluations(self):
        """View evaluations using this template"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations',
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('template_id', '=', self.id)],
            'context': {'default_template_id': self.id},
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
