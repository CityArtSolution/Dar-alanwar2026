from odoo import models, fields


class EducationLeaveReason(models.Model):
    _name = 'education.leave.reason'
    _description = 'Leave Reason'

    name = fields.Char(string='Reason', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)
