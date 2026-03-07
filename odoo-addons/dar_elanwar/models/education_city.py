# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationCity(models.Model):
    _name = 'education.city'
    _description = 'City'
    _order = 'name'

    name = fields.Char(
        string='City Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    country_id = fields.Many2one(
        'res.country',
        string='Country',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    student_ids = fields.One2many(
        'education.student',
        'city_id',
        string='Students',
    )
    parent_ids = fields.One2many(
        'res.partner',
        'guardian_city_id',
        string='Parents',
    )

    # Computed counts
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_counts',
    )
    parent_count = fields.Integer(
        string='Parent Count',
        compute='_compute_counts',
    )

    @api.depends('student_ids', 'parent_ids')
    def _compute_counts(self):
        for record in self:
            record.student_count = len(record.student_ids)
            record.parent_count = len(record.parent_ids)

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'education.student',
            'view_mode': 'list,form',
            'domain': [('city_id', '=', self.id)],
            'context': {'default_city_id': self.id},
        }

    def action_view_parents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Guardians',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('is_guardian', '=', True), ('guardian_city_id', '=', self.id)],
            'context': {'default_guardian_city_id': self.id, 'default_is_guardian': True},
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'City name must be unique!'),
    ]
