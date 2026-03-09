# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DarPortalUserSetPasswordWizard(models.TransientModel):
    _name = 'dar.portal.user.set.password.wizard'
    _description = 'Set Portal User Password'

    portal_user_id = fields.Many2one(
        'dar.portal.user',
        string='Portal User',
        required=True,
    )
    new_password = fields.Char(
        string='New Password',
        required=True,
    )
    confirm_password = fields.Char(
        string='Confirm Password',
        required=True,
    )

    def action_set_password(self):
        """Set the password for the portal user."""
        self.ensure_one()
        if self.new_password != self.confirm_password:
            raise ValidationError(_('Passwords do not match.'))
        self.portal_user_id.set_password(self.new_password)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Password Updated'),
                'message': _('Password has been set successfully.'),
                'type': 'success',
            },
        }
