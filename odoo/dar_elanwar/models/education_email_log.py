# -*- coding: utf-8 -*-

from odoo import models, fields, api

EMAIL_STATUS = [
    ('pending', 'Pending'),
    ('sent', 'Sent'),
    ('failed', 'Failed'),
]


class EducationEmailLog(models.Model):
    _name = 'education.email.log'
    _description = 'Email Log'
    _order = 'create_date desc'

    message_id = fields.Many2one(
        'education.message',
        string='Message',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
    )
    email = fields.Char(
        string='Email Address',
    )
    sent_date = fields.Datetime(
        string='Sent Date',
    )
    status = fields.Selection(
        selection=EMAIL_STATUS,
        string='Status',
        default='pending',
    )
    error_message = fields.Text(
        string='Error Message',
    )

    # Related
    parent_name = fields.Char(
        string='Parent Name',
        related='student_id.father_id.name',
    )

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.message_id.name} - {record.student_id.name}"
            result.append((record.id, name))
        return result
