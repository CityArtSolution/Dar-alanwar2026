# -*- coding: utf-8 -*-

import logging

from odoo import http
from odoo.http import request

from .api_base import admin_jwt_required, json_response

_logger = logging.getLogger(__name__)


class PortalUsersApiController(http.Controller):

    @http.route('/api/admin/portal-accounts', type='http', auth='none',
                methods=['GET', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def list_portal_users(self, **kwargs):
        """List all portal users with search/filter/pagination."""
        page = int(kwargs.get('page', 1))
        limit = 20
        offset = (page - 1) * limit
        search = kwargs.get('search', '').strip()
        user_type = kwargs.get('user_type', '')
        status = kwargs.get('status', '')

        domain = []
        if search:
            domain = ['|', '|',
                       ('username', 'ilike', search),
                       ('guardian_name', 'ilike', search),
                       ('partner_id.email', 'ilike', search)]
        if user_type:
            domain.append(('user_type', '=', user_type))
        if status == 'active':
            domain.append(('is_active', '=', True))
        elif status == 'inactive':
            domain.append(('is_active', '=', False))

        PortalUser = request.env['dar.portal.user'].sudo()
        total = PortalUser.search_count(domain)
        users = PortalUser.search(domain, limit=limit, offset=offset, order='create_date desc')

        result = []
        for pu in users:
            result.append({
                'id': pu.id,
                'username': pu.username,
                'name': pu.guardian_name or '',
                'user_type': pu.user_type,
                'is_active': pu.is_active,
                'last_login': str(pu.last_login) if pu.last_login else '',
                'login_count': pu.login_count,
                'partner_id': pu.partner_id.id,
                'email': pu.partner_id.email or '',
                'phone': pu.partner_id.phone or '',
                'create_date': str(pu.create_date)[:10] if pu.create_date else '',
            })

        return json_response({
            'users': result,
            'total': total,
            'pages': (total + limit - 1) // limit,
            'page': page,
        })
