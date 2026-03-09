# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationBus(models.Model):
    _name = 'education.bus'
    _description = 'School Bus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Bus Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Code',
        required=True,
    )
    plate_number = fields.Char(
        string='Plate Number',
        required=True,
    )
    capacity = fields.Integer(
        string='Capacity',
        required=True,
        default=30,
    )
    driver_id = fields.Many2one(
        'education.driver',
        string='Assigned Driver',
    )
    supervisor_name = fields.Char(
        string='Supervisor Name',
    )
    supervisor_phone = fields.Char(
        string='Supervisor Phone',
    )
    model = fields.Char(
        string='Vehicle Model',
    )
    year = fields.Char(
        string='Year',
    )
    color = fields.Char(
        string='Color',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related routes
    route_ids = fields.One2many(
        'education.bus.route',
        'bus_id',
        string='Routes',
    )

    # Related student assignments
    transport_ids = fields.One2many(
        'education.student.transport',
        'bus_id',
        string='Student Assignments',
    )

    # Computed
    student_count = fields.Integer(
        string='Assigned Students',
        compute='_compute_student_count',
    )
    available_seats = fields.Integer(
        string='Available Seats',
        compute='_compute_student_count',
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Bus code must be unique!'),
        ('plate_unique', 'UNIQUE(plate_number)', 'Plate number must be unique!'),
    ]

    route_count = fields.Integer(
        string='Routes',
        compute='_compute_route_count',
    )

    @api.depends('route_ids')
    def _compute_route_count(self):
        for record in self:
            record.route_count = len(record.route_ids)

    @api.depends('transport_ids', 'capacity')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.transport_ids)
            record.available_seats = record.capacity - record.student_count

    # Stat button actions
    def action_view_students(self):
        """View students assigned to this bus"""
        self.ensure_one()
        student_ids = self.transport_ids.mapped('student_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('id', 'in', student_ids)],
        }

    def action_view_routes(self):
        """View bus routes"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Routes',
            'res_model': 'education.bus.route',
            'view_mode': 'list,form',
            'domain': [('bus_id', '=', self.id)],
            'context': {'default_bus_id': self.id},
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
