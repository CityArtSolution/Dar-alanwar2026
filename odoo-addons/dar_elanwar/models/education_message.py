# -*- coding: utf-8 -*-

from odoo import models, fields, api

RECIPIENT_TYPES = [
    ('all', 'All Parents'),
    ('department', 'By Department'),
    ('class', 'By Class'),
    ('individual', 'Individual Students'),
]

MESSAGE_STATES = [
    ('draft', 'Draft'),
    ('scheduled', 'Scheduled'),
    ('sent', 'Sent'),
    ('cancelled', 'Cancelled'),
]


class EducationMessage(models.Model):
    _name = 'education.message'
    _description = 'Message'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        copy=False,
        default='New',
    )
    template_id = fields.Many2one(
        'education.message.template',
        string='Template',
    )
    recipient_type = fields.Selection(
        selection=RECIPIENT_TYPES,
        string='Recipient Type',
        default='all',
        required=True,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        domain="[('department_id', '=', department_id)]",
    )
    student_ids = fields.Many2many(
        'education.student',
        'education_message_student_rel',
        'message_id',
        'student_id',
        string='Students',
    )
    subject = fields.Char(
        string='Subject',
        required=True,
    )
    body = fields.Html(
        string='Body',
        required=True,
    )
    scheduled_date = fields.Datetime(
        string='Scheduled Date',
    )
    sent_date = fields.Datetime(
        string='Sent Date',
    )
    state = fields.Selection(
        selection=MESSAGE_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
    )

    # Related logs
    log_ids = fields.One2many(
        'education.email.log',
        'message_id',
        string='Email Logs',
    )

    # Computed
    recipient_count = fields.Integer(
        string='Recipient Count',
        compute='_compute_recipient_count',
    )
    sent_count = fields.Integer(
        string='Sent Count',
        compute='_compute_sent_count',
    )

    @api.depends('recipient_type', 'department_id', 'class_id', 'student_ids')
    def _compute_recipient_count(self):
        for record in self:
            if record.recipient_type == 'all':
                record.recipient_count = self.env['education.student'].search_count([('state', '=', 'enrolled')])
            elif record.recipient_type == 'department':
                record.recipient_count = self.env['education.student'].search_count([
                    ('department_id', '=', record.department_id.id),
                    ('state', '=', 'enrolled'),
                ])
            elif record.recipient_type == 'class':
                record.recipient_count = self.env['education.student'].search_count([
                    ('class_id', '=', record.class_id.id),
                    ('state', '=', 'enrolled'),
                ])
            elif record.recipient_type == 'individual':
                record.recipient_count = len(record.student_ids)
            else:
                record.recipient_count = 0

    @api.depends('log_ids.status')
    def _compute_sent_count(self):
        for record in self:
            record.sent_count = len(record.log_ids.filtered(lambda l: l.status == 'sent'))

    failed_count = fields.Integer(
        string='Failed Count',
        compute='_compute_log_counts',
    )
    log_count = fields.Integer(
        string='Log Count',
        compute='_compute_log_counts',
    )

    @api.depends('log_ids', 'log_ids.status')
    def _compute_log_counts(self):
        for record in self:
            record.log_count = len(record.log_ids)
            record.failed_count = len(record.log_ids.filtered(lambda l: l.status == 'failed'))

    # Stat button actions
    def action_view_logs(self):
        """View email logs for this message"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Email Logs',
            'res_model': 'education.email.log',
            'view_mode': 'list,form',
            'domain': [('message_id', '=', self.id)],
            'context': {'default_message_id': self.id},
        }

    def action_view_students(self):
        """View students for this message"""
        self.ensure_one()
        student_ids = self.student_ids.ids
        if self.recipient_type == 'all':
            return {
                'type': 'ir.actions.act_window',
                'name': 'Students',
                'res_model': 'education.student',
                'view_mode': 'list,form',
                'domain': [('state', '=', 'enrolled')],
            }
        elif self.recipient_type == 'department':
            return {
                'type': 'ir.actions.act_window',
                'name': 'Students',
                'res_model': 'education.student',
                'view_mode': 'list,form',
                'domain': [('department_id', '=', self.department_id.id), ('state', '=', 'enrolled')],
            }
        elif self.recipient_type == 'class':
            return {
                'type': 'ir.actions.act_window',
                'name': 'Students',
                'res_model': 'education.student',
                'view_mode': 'list,form',
                'domain': [('class_id', '=', self.class_id.id), ('state', '=', 'enrolled')],
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Students',
                'res_model': 'education.student',
                'view_mode': 'list,form',
                'domain': [('id', 'in', student_ids)],
            }

    def action_view_failed(self):
        """View failed email logs"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Failed Emails',
            'res_model': 'education.email.log',
            'view_mode': 'list,form',
            'domain': [('message_id', '=', self.id), ('status', '=', 'failed')],
        }

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.subject = self.template_id.subject
            self.body = self.template_id.body

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('education.message') or 'New'
        return super().create(vals_list)

    def action_send(self):
        """Send the message to recipients"""
        for record in self:
            # Get recipients based on type
            if record.recipient_type == 'all':
                students = self.env['education.student'].search([('state', '=', 'enrolled')])
            elif record.recipient_type == 'department':
                students = self.env['education.student'].search([
                    ('department_id', '=', record.department_id.id),
                    ('state', '=', 'enrolled'),
                ])
            elif record.recipient_type == 'class':
                students = self.env['education.student'].search([
                    ('class_id', '=', record.class_id.id),
                    ('state', '=', 'enrolled'),
                ])
            else:
                students = record.student_ids

            # Create log entries for each recipient
            for student in students:
                self.env['education.email.log'].create({
                    'message_id': record.id,
                    'student_id': student.id,
                    'email': student.father_id.email or student.mother_id.email or '',
                    'status': 'pending',
                })

            record.write({
                'state': 'sent',
                'sent_date': fields.Datetime.now(),
            })

    def action_cancel(self):
        """Cancel the message"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
