# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

PERIOD_TYPES = [
    ('morning', 'Morning / صباحي'),
    ('afternoon', 'Afternoon / مسائي'),
    ('evening', 'Evening / ليلي'),
    ('full_day', 'Full Day / يوم كامل'),
]


class EducationSchedule(models.Model):
    _name = 'education.schedule'
    _description = 'Education Schedule'
    _order = 'time_from'

    name = fields.Char(
        string='Schedule Name',
        required=True,
    )
    time_from = fields.Float(
        string='From',
        required=True,
        help='Start time in 24-hour format (e.g., 8.0 for 8:00 AM)',
    )
    time_to = fields.Float(
        string='To',
        required=True,
        help='End time in 24-hour format (e.g., 14.0 for 2:00 PM)',
    )
    period = fields.Selection(
        selection=PERIOD_TYPES,
        string='Period',
        required=True,
    )
    display_time = fields.Char(
        string='Display Time',
        compute='_compute_display_time',
        store=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.depends('time_from', 'time_to')
    def _compute_display_time(self):
        for record in self:
            from_hours = int(record.time_from)
            from_minutes = int((record.time_from - from_hours) * 60)
            to_hours = int(record.time_to)
            to_minutes = int((record.time_to - to_hours) * 60)
            record.display_time = f"{from_hours:02d}:{from_minutes:02d} - {to_hours:02d}:{to_minutes:02d}"

    @api.constrains('time_from', 'time_to')
    def _check_times(self):
        for record in self:
            if record.time_from >= record.time_to:
                raise ValidationError('End time must be after start time!')
            if record.time_from < 0 or record.time_from > 24:
                raise ValidationError('Start time must be between 0 and 24!')
            if record.time_to < 0 or record.time_to > 24:
                raise ValidationError('End time must be between 0 and 24!')

    def _compute_display_name(self):
        for record in self:
            name = f"{record.name} ({record.display_time})"
            record.display_name = name
