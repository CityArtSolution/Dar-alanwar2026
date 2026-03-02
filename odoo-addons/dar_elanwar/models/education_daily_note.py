# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationDailyNote(models.Model):
    _name = 'education.daily.note'
    _description = 'Daily Note'
    _order = 'date desc, id desc'

    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
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
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
