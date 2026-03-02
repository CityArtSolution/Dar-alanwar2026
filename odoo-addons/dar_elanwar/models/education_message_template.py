# -*- coding: utf-8 -*-

from odoo import models, fields, api

TRIGGER_TYPES = [
    ('manual', 'Manual'),
    ('payment_due', 'Payment Due'),
    ('payment_overdue', 'Payment Overdue'),
    ('attendance_absent', 'Absent Notification'),
    ('evaluation_ready', 'Evaluation Ready'),
    ('welcome', 'Welcome Message'),
    ('other', 'Other'),
]


class EducationMessageTemplate(models.Model):
    _name = 'education.message.template'
    _description = 'Message Template'
    _order = 'name'

    name = fields.Char(
        string='Template Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    subject = fields.Char(
        string='Subject',
        required=True,
    )
    body = fields.Html(
        string='Body',
        required=True,
    )
    trigger_type = fields.Selection(
        selection=TRIGGER_TYPES,
        string='Trigger Type',
        default='manual',
        required=True,
    )
    is_email = fields.Boolean(
        string='Send Email',
        default=True,
    )
    is_sms = fields.Boolean(
        string='Send SMS',
        default=False,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related records
    message_ids = fields.One2many(
        'education.message',
        'template_id',
        string='Messages',
    )

    # Computed counts
    message_count = fields.Integer(
        string='Message Count',
        compute='_compute_message_count',
    )
    sent_count = fields.Integer(
        string='Sent Count',
        compute='_compute_message_count',
    )

    @api.depends('message_ids', 'message_ids.state')
    def _compute_message_count(self):
        for record in self:
            record.message_count = len(record.message_ids)
            record.sent_count = len(record.message_ids.filtered(lambda m: m.state == 'sent'))

    def action_view_messages(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Messages',
            'res_model': 'education.message',
            'view_mode': 'list,form',
            'domain': [('template_id', '=', self.id)],
            'context': {'default_template_id': self.id},
        }

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Template code must be unique!'),
    ]
