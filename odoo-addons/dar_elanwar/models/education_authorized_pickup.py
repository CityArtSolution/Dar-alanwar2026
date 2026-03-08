# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationAuthorizedPickup(models.Model):
    _name = 'education.authorized.pickup'
    _description = 'Authorized Pickup Person'
    _order = 'student_id, name'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        ondelete='cascade',
        domain=[('is_student', '=', True)],
    )
    name = fields.Char(
        string='Full Name',
        required=True,
    )
    relation = fields.Char(
        string='Relation',
        help='Relation to the student (e.g., Uncle, Driver, etc.)',
    )
    phone = fields.Char(
        string='Phone',
        required=True,
    )
    id_number = fields.Char(
        string='ID Number',
    )
    photo = fields.Binary(
        string='Photo',
        attachment=True,
    )
    notes = fields.Text(
        string='Notes',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.relation:
                name = f"{record.name} ({record.relation})"
            result.append((record.id, name))
        return result
