# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationDriver(models.Model):
    _name = 'education.driver'
    _description = 'Driver'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Driver Name',
        required=True,
        tracking=True,
    )
    phone = fields.Char(
        string='Phone',
        required=True,
    )
    mobile = fields.Char(
        string='Mobile',
    )
    license_number = fields.Char(
        string='License Number',
        required=True,
    )
    license_expiry = fields.Date(
        string='License Expiry Date',
    )
    id_number = fields.Char(
        string='ID Number',
    )
    photo = fields.Binary(
        string='Photo',
        attachment=True,
    )
    address = fields.Text(
        string='Address',
    )
    hire_date = fields.Date(
        string='Hire Date',
        default=fields.Date.context_today,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related buses
    bus_ids = fields.One2many(
        'education.bus',
        'driver_id',
        string='Assigned Buses',
    )

    # Computed
    bus_count = fields.Integer(
        string='Bus Count',
        compute='_compute_bus_count',
    )

    _license_unique = models.Constraint(
        'UNIQUE(license_number)',
        'License number must be unique!',
    )

    student_count = fields.Integer(
        string='Students',
        compute='_compute_counts',
    )
    route_count = fields.Integer(
        string='Routes',
        compute='_compute_counts',
    )
    transport_count = fields.Integer(
        string='Transport Records',
        compute='_compute_counts',
    )

    @api.depends('bus_ids')
    def _compute_bus_count(self):
        for record in self:
            record.bus_count = len(record.bus_ids)

    @api.depends('bus_ids')
    def _compute_counts(self):
        for record in self:
            # Count students from all buses this driver handles
            record.student_count = sum(bus.student_count for bus in record.bus_ids)
            # Count routes from all buses
            record.route_count = sum(len(bus.route_ids) for bus in record.bus_ids)
            # Count transport records
            record.transport_count = self.env['education.student.transport'].search_count([
                ('bus_id', 'in', record.bus_ids.ids)
            ])

    # Stat button actions
    def action_view_buses(self):
        """View buses assigned to this driver"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buses',
            'res_model': 'education.bus',
            'view_mode': 'list,form',
            'domain': [('driver_id', '=', self.id)],
            'context': {'default_driver_id': self.id},
        }

    def action_view_students(self):
        """View students transported by this driver"""
        self.ensure_one()
        transport_records = self.env['education.student.transport'].search([
            ('bus_id', 'in', self.bus_ids.ids)
        ])
        student_ids = transport_records.mapped('student_id').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'res.partner',
            'view_mode': 'list,kanban,form',
            'domain': [('id', 'in', student_ids)],
        }

    def action_view_routes(self):
        """View routes for this driver's buses"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Routes',
            'res_model': 'education.bus.route',
            'view_mode': 'list,form',
            'domain': [('bus_id', 'in', self.bus_ids.ids)],
        }

    def action_view_transport(self):
        """View transport records for this driver"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transport Records',
            'res_model': 'education.student.transport',
            'view_mode': 'list,form',
            'domain': [('bus_id', 'in', self.bus_ids.ids)],
        }
