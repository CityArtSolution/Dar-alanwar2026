# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationLevel(models.Model):
    _name = 'education.level'
    _description = 'Education Level'
    _order = 'department_id, sequence, name'

    name = fields.Char(
        string='Level Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
        ondelete='cascade',
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    class_ids = fields.One2many(
        'education.class',
        'level_id',
        string='Classes',
    )

    # Computed
    class_count = fields.Integer(
        string='Class Count',
        compute='_compute_class_count',
    )

    _sql_constraints = [
        ('code_department_unique', 'UNIQUE(code, department_id)',
         'Level code must be unique within department!'),
    ]

    student_count = fields.Integer(
        string='Students',
        compute='_compute_counts',
    )

    @api.depends('class_ids')
    def _compute_class_count(self):
        for record in self:
            record.class_count = len(record.class_ids)

    def _compute_counts(self):
        for record in self:
            record.student_count = self.env['education.student'].search_count([
                ('level_id', '=', record.id)
            ])

    # Stat button actions
    def action_view_classes(self):
        """View level classes"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Classes',
            'res_model': 'education.class',
            'view_mode': 'list,form',
            'domain': [('level_id', '=', self.id)],
            'context': {'default_level_id': self.id, 'default_department_id': self.department_id.id},
        }

    def action_view_students(self):
        """View level students"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'education.student',
            'view_mode': 'list,kanban,form',
            'domain': [('level_id', '=', self.id)],
        }

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.department_id:
                name = f"{record.department_id.name} / {record.name}"
            result.append((record.id, name))
        return result
