# -*- coding: utf-8 -*-

import string
import secrets
import logging

from werkzeug.security import generate_password_hash, check_password_hash

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DarPortalUser(models.Model):
    _name = 'dar.portal.user'
    _description = 'Parent Portal User Account'
    _order = 'create_date desc'
    _rec_name = 'username'

    partner_id = fields.Many2one(
        'res.partner',
        string='Guardian',
        required=True,
        ondelete='cascade',
        domain=[('is_guardian', '=', True)],
        index=True,
    )
    guardian_name = fields.Char(
        related='partner_id.name',
        string='Guardian Name',
        store=True,
    )
    username = fields.Char(
        string='Username (Phone)',
        required=True,
        index=True,
    )
    password_hash = fields.Char(
        string='Password Hash',
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
    )
    last_login = fields.Datetime(
        string='Last Login',
        readonly=True,
    )
    login_count = fields.Integer(
        string='Login Count',
        default=0,
        readonly=True,
    )
    notes = fields.Text(
        string='Notes',
    )
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )

    _sql_constraints = [
        ('username_unique', 'UNIQUE(username)',
         'A portal user with this username already exists.'),
        ('partner_unique', 'UNIQUE(partner_id)',
         'This guardian already has a portal account.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('username') and vals.get('partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                if partner.phone:
                    vals['username'] = partner.phone.strip()
        return super().create(vals_list)

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id and self.partner_id.phone:
            self.username = self.partner_id.phone.strip()

    def set_password(self, password):
        """Set a hashed password for this portal user."""
        self.ensure_one()
        if not password or len(password) < 6:
            raise ValidationError(_('Password must be at least 6 characters.'))
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify a password against the stored hash."""
        self.ensure_one()
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def action_generate_password(self):
        """Generate a random password and show it to the admin."""
        self.ensure_one()
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for _ in range(10))
        self.set_password(password)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Password Generated'),
                'message': _('New password: %s\nPlease share it securely with the guardian.') % password,
                'type': 'warning',
                'sticky': True,
            },
        }

    def action_toggle_active(self):
        """Toggle the active status of this portal user."""
        self.ensure_one()
        self.is_active = not self.is_active
        status = _('activated') if self.is_active else _('deactivated')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Portal Account %s') % status,
                'message': _('Portal account for %s has been %s.') % (self.guardian_name, status),
                'type': 'success',
            },
        }

    def action_set_password(self):
        """Open the set password wizard."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Set Password'),
            'res_model': 'dar.portal.user.set.password.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_portal_user_id': self.id},
        }

    def record_login(self):
        """Record a successful login."""
        self.ensure_one()
        self.sudo().write({
            'last_login': fields.Datetime.now(),
            'login_count': self.login_count + 1,
        })
