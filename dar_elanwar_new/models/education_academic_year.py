from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EducationAcademicYear(models.Model):
    _name = 'education.academic.year'
    _description = 'Academic Year'
    _order = 'date_start desc'

    name = fields.Char(string='Academic Year', required=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    is_current = fields.Boolean(string='Current Year', default=False)
    active = fields.Boolean(default=True)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start >= rec.date_end:
                raise ValidationError(_('End date must be after start date.'))

    @api.constrains('is_current')
    def _check_current_year(self):
        for rec in self:
            if rec.is_current:
                others = self.search([
                    ('is_current', '=', True),
                    ('id', '!=', rec.id),
                ])
                if others:
                    raise ValidationError(
                        _('Only one academic year can be set as current.'))
