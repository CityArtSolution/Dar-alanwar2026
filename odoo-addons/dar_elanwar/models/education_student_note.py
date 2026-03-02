# -*- coding: utf-8 -*-

from odoo import models, fields

NOTE_TYPES = [
    ('general', 'General'),
    ('behavior', 'Behavior'),
    ('academic', 'Academic'),
    ('health', 'Health'),
    ('payment', 'Payment'),
    ('communication', 'Communication'),
]


class EducationStudentNote(models.Model):
    _name = 'education.student.note'
    _description = 'Student Note'
    _order = 'date desc, id desc'

    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
    )
    note_type = fields.Selection(
        selection=NOTE_TYPES,
        string='Type',
        default='general',
    )
    note = fields.Text(
        string='Note',
        required=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    is_important = fields.Boolean(
        string='Important',
        default=False,
    )
    color = fields.Integer(
        string='Color',
    )
