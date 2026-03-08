# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date


class EducationSibling(models.Model):
    _name = 'education.sibling'
    _description = 'Student Sibling'
    _order = 'student_id, birthdate'

    student_id = fields.Many2one(
        'res.partner',
        string='Student',
        required=True,
        ondelete='cascade',
        domain=[('is_student', '=', True)],
    )
    name = fields.Char(
        string='Sibling Name',
        required=True,
    )
    birthdate = fields.Date(
        string='Birth Date',
    )
    gender = fields.Selection([
        ('male', 'Male / ذكر'),
        ('female', 'Female / أنثى'),
    ], string='Gender')
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    is_enrolled = fields.Boolean(
        string='Enrolled in Institution',
        default=False,
    )
    enrolled_student_id = fields.Many2one(
        'res.partner',
        string='Enrolled As',
        help='Link to student record if sibling is also enrolled',
        domain=[('is_student', '=', True)],
    )
    notes = fields.Text(
        string='Notes',
    )

    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birthdate:
                delta = relativedelta(today, record.birthdate)
                record.age = f"{delta.years} years"
            else:
                record.age = ''
