# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationBusRoute(models.Model):
    _name = 'education.bus.route'
    _description = 'Bus Route'
    _order = 'bus_id, sequence'

    name = fields.Char(
        string='Route Name',
        required=True,
    )
    bus_id = fields.Many2one(
        'education.bus',
        string='Bus',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    route_type = fields.Selection([
        ('pickup', 'Pickup'),
        ('dropoff', 'Drop-off'),
        ('both', 'Both'),
    ], string='Route Type', default='both', required=True)
    start_location = fields.Char(
        string='Start Location',
    )
    end_location = fields.Char(
        string='End Location',
    )
    stops = fields.Text(
        string='Stops',
        help='List of stops on this route',
    )
    departure_time = fields.Float(
        string='Departure Time',
    )
    arrival_time = fields.Float(
        string='Arrival Time',
    )
    distance_km = fields.Float(
        string='Distance (km)',
    )
    duration_minutes = fields.Integer(
        string='Duration (minutes)',
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related
    driver_id = fields.Many2one(
        'education.driver',
        string='Driver',
        related='bus_id.driver_id',
        store=True,
    )

    # Computed counts
    student_count = fields.Integer(
        string='Students',
        compute='_compute_student_count',
    )

    @api.depends('bus_id')
    def _compute_student_count(self):
        for record in self:
            record.student_count = record.bus_id.student_count if record.bus_id else 0

    # Stat button actions
    def action_view_bus(self):
        """View the bus for this route"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Bus',
            'res_model': 'education.bus',
            'view_mode': 'form',
            'res_id': self.bus_id.id,
        }

    def action_view_driver(self):
        """View the driver for this route"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Driver',
            'res_model': 'education.driver',
            'view_mode': 'form',
            'res_id': self.driver_id.id,
        }

    def action_view_students(self):
        """View students on this route's bus"""
        self.ensure_one()
        transport_records = self.env['education.student.transport'].search([
            ('bus_id', '=', self.bus_id.id)
        ])
        student_ids = transport_records.mapped('student_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('id', 'in', student_ids)],
        }

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.bus_id.name} - {record.name}"
            result.append((record.id, name))
        return result
