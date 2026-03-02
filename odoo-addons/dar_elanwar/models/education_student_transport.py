# -*- coding: utf-8 -*-

from odoo import models, fields, api

PICKUP_METHODS = [
    ('self', 'Self'),
    ('parent', 'Parent/Guardian'),
    ('authorized', 'Authorized Person'),
    ('bus', 'School Bus'),
]


class EducationStudentTransport(models.Model):
    _name = 'education.student.transport'
    _description = 'Student Transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'student_id'

    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
        ondelete='cascade',
    )
    pickup_method = fields.Selection(
        selection=PICKUP_METHODS,
        string='Pickup Method',
        default='parent',
        required=True,
        tracking=True,
    )
    dropoff_method = fields.Selection(
        selection=PICKUP_METHODS,
        string='Drop-off Method',
        default='parent',
        required=True,
        tracking=True,
    )
    bus_id = fields.Many2one(
        'education.bus',
        string='Bus',
        help='Assigned bus for transportation',
    )
    driver_id = fields.Many2one(
        'education.driver',
        string='Driver',
        related='bus_id.driver_id',
        store=True,
    )
    pickup_address = fields.Text(
        string='Pickup Address',
    )
    dropoff_address = fields.Text(
        string='Drop-off Address',
    )
    pickup_time = fields.Float(
        string='Pickup Time',
    )
    dropoff_time = fields.Float(
        string='Drop-off Time',
    )
    transport_fee = fields.Float(
        string='Monthly Transport Fee',
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    notes = fields.Text(
        string='Notes',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related fields
    parent_id = fields.Many2one(
        'education.parent',
        string='Parent',
        related='student_id.father_id',
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        related='student_id.class_id',
        store=True,
    )

    _sql_constraints = [
        ('student_unique', 'UNIQUE(student_id)', 'Each student can only have one transport assignment!'),
    ]

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.student_id.name} - {record.pickup_method}"
            result.append((record.id, name))
        return result
