# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationReminder(models.Model):
    _name = 'education.reminder'
    _description = 'Reminder'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date, time'

    title = fields.Char(
        string='Title',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
    )
    date = fields.Date(
        string='Date',
        required=True,
        tracking=True,
    )
    time = fields.Float(
        string='Time',
        help='Time in 24-hour format (e.g., 14.5 for 2:30 PM)',
    )
    is_done = fields.Boolean(
        string='Done',
        default=False,
        tracking=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        default=lambda self: self.env.user,
        tracking=True,
    )
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='1')
    color = fields.Integer(
        string='Color',
        compute='_compute_color',
        store=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.depends('is_done', 'priority')
    def _compute_color(self):
        """Compute color based on status and priority"""
        for record in self:
            if record.is_done:
                record.color = 10  # Green
            elif record.priority == '3':
                record.color = 1  # Red
            elif record.priority == '2':
                record.color = 3  # Yellow
            else:
                record.color = 0  # Default

    def action_mark_done(self):
        """Mark reminder as done"""
        self.write({'is_done': True})

    def action_mark_undone(self):
        """Mark reminder as not done"""
        self.write({'is_done': False})
