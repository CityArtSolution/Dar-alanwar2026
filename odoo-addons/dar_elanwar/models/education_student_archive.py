# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationStudentArchive(models.Model):
    _name = 'education.student.archive'
    _description = 'Student Archive History'
    _order = 'archive_date desc'

    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    archive_date = fields.Date(
        string='Archive Date',
        required=True,
        default=fields.Date.context_today,
    )
    reason_id = fields.Many2one(
        'education.leave.reason',
        string='Leave Reason',
        required=True,
    )
    return_date = fields.Date(
        string='Return Date',
    )
    notes = fields.Text(
        string='Notes',
    )
    user_id = fields.Many2one(
        'res.users',
        string='Archived By',
        default=lambda self: self.env.user,
        readonly=True,
    )

    # Store state at archive time
    department_id = fields.Many2one(
        'education.department',
        string='Department at Archive',
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class at Archive',
    )
