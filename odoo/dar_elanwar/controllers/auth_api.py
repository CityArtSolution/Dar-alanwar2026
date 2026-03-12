import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    generate_jwt_token, get_request_data, jwt_required,
)

_logger = logging.getLogger(__name__)


class AuthApiController(ApiBaseController):

    @http.route('/api/auth/login', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    def login(self, **kwargs):
        """Authenticate a parent via portal user account."""
        data = get_request_data()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()

        if not password or (not email and not phone):
            return error_response('Email/phone and password are required')

        # Look up portal user by username (phone) or by partner email
        portal_user = None
        if phone:
            portal_user = request.env['dar.portal.user'].sudo().search(
                [('username', '=', phone)], limit=1)
        elif email:
            portal_user = request.env['dar.portal.user'].sudo().search(
                [('partner_id.email', '=', email)], limit=1)

        if not portal_user:
            return error_response('Invalid credentials', 401)

        if not portal_user.is_active:
            return error_response('Account is disabled. Contact administration.', 401,
                                  'ACCOUNT_DISABLED')

        if not portal_user.verify_password(password):
            return error_response('Invalid credentials', 401)

        partner = portal_user.partner_id
        user_type = portal_user.user_type or 'parent'
        portal_user.record_login()

        token = generate_jwt_token(partner.id, partner.email or '',
                                   portal_user_id=portal_user.id,
                                   user_type=user_type)

        response_data = {
            'success': True,
            'token': token,
            'user_type': user_type,
            'parent': {
                'id': partner.id,
                'name': partner.name,
                'email': partner.email,
                'phone': partner.phone,
                'relation': getattr(partner, 'guardian_relation', None),
            },
        }

        # Only include children for parent users
        if user_type == 'parent':
            children = self._get_parent_children(partner)
            response_data['children'] = [self._serialize_student(c) for c in children]
        else:
            response_data['children'] = []

        return json_response(response_data)

    @http.route('/api/auth/refresh', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def refresh_token(self, **kwargs):
        """Refresh JWT token."""
        partner = request.parent
        portal_user = getattr(request, 'portal_user', None)
        user_type = portal_user.user_type if portal_user else 'parent'
        token = generate_jwt_token(
            partner.id, partner.email or '',
            portal_user_id=portal_user.id if portal_user else None,
            user_type=user_type,
        )
        return json_response({
            'success': True,
            'token': token,
            'user_type': user_type,
        })

    @http.route('/api/auth/profile', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_profile(self, **kwargs):
        """Get current parent profile."""
        parent = request.parent
        return json_response({
            'id': parent.id,
            'name': parent.name,
            'email': parent.email,
            'phone': parent.phone,
            'mobile': parent.mobile,
            'relation': parent.guardian_relation,
            'nationality': parent.country_id.name if parent.country_id else None,
            'job': parent.function,
            'workplace': parent.workplace,
            'children_count': parent.children_count,
            'children_balance_due': parent.children_balance_due,
        })

    @http.route('/api/auth/password', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def change_password(self, **kwargs):
        """Change portal user password."""
        data = get_request_data()
        new_password = data.get('new_password', '')
        if len(new_password) < 6:
            return error_response('Password must be at least 6 characters')

        portal_user = getattr(request, 'portal_user', None)
        if portal_user:
            portal_user.sudo().set_password(new_password)
        else:
            # Legacy fallback for old tokens without portal_user_id
            parent = request.parent
            portal_user = request.env['dar.portal.user'].sudo().search(
                [('partner_id', '=', parent.id)], limit=1)
            if portal_user:
                portal_user.set_password(new_password)
            else:
                return error_response('No portal account found', 404)

        return json_response({'success': True, 'message': 'Password updated'})
