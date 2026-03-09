# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationEmployeeQualification(models.Model):
    _name = 'education.employee.qualification'
    _description = 'Employee Qualification'
    _order = 'date desc'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Qualification Name',
        required=True,
    )
    institution = fields.Char(
        string='Institution',
    )
    date = fields.Date(
        string='Date Obtained',
    )
    certificate = fields.Binary(
        string='Certificate',
        attachment=True,
    )
    certificate_filename = fields.Char(
        string='Certificate Filename',
    )
    notes = fields.Text(
        string='Notes',
    )
