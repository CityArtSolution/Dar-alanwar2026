import hashlib
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
        """Authenticate a parent and return a JWT token."""
        data = get_request_data()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        phone = data.get('phone', '').strip()

        if not password or (not email and not phone):
            return error_response('Email/phone and password are required')

        domain = []
        if email:
            domain = [('email', '=', email)]
        elif phone:
            domain = ['|', ('phone', '=', phone), ('mobile', '=', phone)]

        parent = request.env['res.partner'].sudo().search(
            [('is_guardian', '=', True)] + domain, limit=1)
        if not parent:
            return error_response('Invalid credentials', 401)

        # Verify password (stored as hashed id_number for simplicity)
        # In production, use proper password hashing
        expected = hashlib.sha256(
            (parent.id_number or str(parent.id)).encode()
        ).hexdigest()
        provided = hashlib.sha256(password.encode()).hexdigest()

        if expected != provided:
            # Fallback: allow id_number as password for initial setup
            if password != parent.id_number and password != str(parent.id):
                return error_response('Invalid credentials', 401)

        token = generate_jwt_token(parent.id, parent.email or '')
        children = self._get_parent_children(parent)

        return json_response({
            'success': True,
            'token': token,
            'parent': {
                'id': parent.id,
                'name': parent.name,
                'email': parent.email,
                'phone': parent.phone,
                'relation': parent.guardian_relation,
            },
            'children': [self._serialize_student(c) for c in children],
        })

    @http.route('/api/auth/refresh', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def refresh_token(self, **kwargs):
        """Refresh JWT token."""
        parent = request.parent
        token = generate_jwt_token(parent.id, parent.email or '')
        return json_response({
            'success': True,
            'token': token,
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
        """Change parent password."""
        data = get_request_data()
        new_password = data.get('new_password', '')
        if len(new_password) < 6:
            return error_response('Password must be at least 6 characters')

        parent = request.parent
        parent.sudo().write({'id_number': new_password})
        return json_response({'success': True, 'message': 'Password updated'})
