# -*- coding: utf-8 -*-

from odoo import models, fields

COMPLAINT_STATUS = [
    ('new', 'New'),
    ('investigating', 'Investigating'),
    ('resolved', 'Resolved'),
    ('dismissed', 'Dismissed'),
]


class EducationEmployeeComplaint(models.Model):
    _name = 'education.employee.complaint'
    _description = 'Employee Complaint'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    employee_id = fields.Many2one(
        'education.employee',
        string='Employee (Subject)',
        required=True,
        ondelete='cascade',
        tracking=True,
        help='The employee the complaint is about',
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    complaint = fields.Text(
        string='Complaint',
        required=True,
    )
    complainant = fields.Char(
        string='Complainant',
        help='Name of the person who filed the complaint',
    )
    complainant_type = fields.Selection([
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('other', 'Other'),
    ], string='Complainant Type')
    status = fields.Selection(
        selection=COMPLAINT_STATUS,
        string='Status',
        default='new',
        tracking=True,
    )
    resolution = fields.Text(
        string='Resolution',
    )
    resolution_date = fields.Date(
        string='Resolution Date',
    )
    assigned_to = fields.Many2one(
        'res.users',
        string='Assigned To',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    def action_investigate(self):
        """Start investigation"""
        self.write({'status': 'investigating'})

    def action_resolve(self):
        """Resolve the complaint"""
        self.write({
            'status': 'resolved',
            'resolution_date': fields.Date.today(),
        })

    def action_dismiss(self):
        """Dismiss the complaint"""
        self.write({'status': 'dismissed'})
