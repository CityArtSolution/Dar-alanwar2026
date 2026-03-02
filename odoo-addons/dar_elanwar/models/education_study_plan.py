# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationStudyPlan(models.Model):
    _name = 'education.study.plan'
    _description = 'Study Plan'
    _order = 'sequence, id'

    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Plan Name',
        required=True,
    )
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
    )
    subject_id = fields.Many2one(
        'education.subject',
        string='Subject',
    )
    teacher_id = fields.Many2one(
        'education.employee',
        string='Teacher',
    )
    schedule = fields.Char(
        string='Schedule',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    notes = fields.Text(
        string='Notes',
    )
