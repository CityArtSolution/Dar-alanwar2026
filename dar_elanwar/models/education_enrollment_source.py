# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationEnrollmentSource(models.Model):
    _name = 'education.enrollment.source'
    _description = 'Enrollment Source'
    _order = 'sequence, name'

    name = fields.Char(
        string='Source Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    student_ids = fields.One2many(
        'res.partner',
        'enrollment_source_id',
        string='Students',
    )

    # Computed counts
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_student_count',
    )

    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)

    def action_view_students(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('enrollment_source_id', '=', self.id)],
            'context': {'default_enrollment_source_id': self.id},
        }

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Enrollment source name must be unique!',
    )
