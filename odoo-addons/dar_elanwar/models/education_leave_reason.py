# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationLeaveReason(models.Model):
    _name = 'education.leave.reason'
    _description = 'Leave Reason'
    _order = 'sequence, name'

    name = fields.Char(
        string='Reason',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    description = fields.Text(
        string='Description',
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
    archive_ids = fields.One2many(
        'education.student.archive',
        'reason_id',
        string='Archives',
    )

    # Computed counts
    archive_count = fields.Integer(
        string='Archive Count',
        compute='_compute_archive_count',
    )
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_archive_count',
    )

    @api.depends('archive_ids')
    def _compute_archive_count(self):
        for record in self:
            record.archive_count = len(record.archive_ids)
            record.student_count = len(record.archive_ids.mapped('student_id'))

    def action_view_archives(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student Archives',
            'res_model': 'education.student.archive',
            'view_mode': 'list,form',
            'domain': [('reason_id', '=', self.id)],
            'context': {'default_reason_id': self.id},
        }

    def action_view_students(self):
        self.ensure_one()
        student_ids = self.archive_ids.mapped('student_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Archived Students',
            'res_model': 'res.partner',
            'view_mode': 'list,form',
            'domain': [('id', 'in', student_ids)],
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Leave reason name must be unique!'),
    ]
