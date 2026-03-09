# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationGradeScale(models.Model):
    _name = 'education.grade.scale'
    _description = 'Grade Scale'
    _order = 'name'

    name = fields.Char(
        string='Scale Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    value_ids = fields.One2many(
        'education.grade.scale.value',
        'scale_id',
        string='Values',
    )

    # Related records
    question_ids = fields.One2many(
        'education.evaluation.question',
        'scale_id',
        string='Questions',
    )

    # Computed
    value_count = fields.Integer(
        string='Value Count',
        compute='_compute_counts',
    )
    question_count = fields.Integer(
        string='Question Count',
        compute='_compute_counts',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Grade scale code must be unique!'),
    ]

    @api.depends('value_ids', 'question_ids')
    def _compute_counts(self):
        for record in self:
            record.value_count = len(record.value_ids)
            record.question_count = len(record.question_ids)

    def action_view_values(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Scale Values',
            'res_model': 'education.grade.scale.value',
            'view_mode': 'list,form',
            'domain': [('scale_id', '=', self.id)],
            'context': {'default_scale_id': self.id},
        }

    def action_view_questions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Questions',
            'res_model': 'education.evaluation.question',
            'view_mode': 'list,form',
            'domain': [('scale_id', '=', self.id)],
            'context': {'default_scale_id': self.id},
        }


class EducationGradeScaleValue(models.Model):
    _name = 'education.grade.scale.value'
    _description = 'Grade Scale Value'
    _order = 'scale_id, sequence'

    name = fields.Char(
        string='Value',
        required=True,
        help='e.g., Excellent, Very Good, Good, Acceptable, Poor',
    )
    scale_id = fields.Many2one(
        'education.grade.scale',
        string='Grade Scale',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    numeric_value = fields.Float(
        string='Numeric Value',
        help='Numeric value for calculation (e.g., 5 for Excellent, 4 for Very Good)',
    )
    color = fields.Integer(
        string='Color',
    )
    description = fields.Char(
        string='Description',
    )

    _sql_constraints = [
        ('name_scale_unique', 'UNIQUE(name, scale_id)',
         'Value name must be unique within scale!'),
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.numeric_value:
                name = f"{record.name} ({record.numeric_value})"
            result.append((record.id, name))
        return result
