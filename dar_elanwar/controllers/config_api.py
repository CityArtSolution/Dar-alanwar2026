import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class ConfigApiController(ApiBaseController):

    @http.route('/api/config', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_config(self, **kwargs):
        """Get portal configuration."""
        ICP = request.env['ir.config_parameter'].sudo()

        return json_response({
            'features': {
                'kids_area': ICP.get_param(
                    'dar_elanwar.enable_kids_area', 'False') == 'True',
                'content_access': ICP.get_param(
                    'dar_elanwar.enable_content_access', 'False') == 'True',
                'transportation': ICP.get_param(
                    'dar_elanwar.enable_transportation', 'False') == 'True',
                'parent_portal': ICP.get_param(
                    'dar_elanwar.enable_parent_portal', 'False') == 'True',
            },
            'academy': {
                'name': 'Dar Al-Anwar Academy',
                'name_ar': 'أكاديمية دار الأنوار',
            },
        })

    @http.route('/api/config/departments', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_departments(self, **kwargs):
        """Get all departments."""
        depts = request.env['education.department'].sudo().search(
            [('active', '=', True)])
        return json_response({
            'departments': [{
                'id': d.id,
                'name': d.name,
                'code': d.code,
                'type': d.type,
                'student_count': d.student_count,
            } for d in depts],
        })

    @http.route('/api/config/branches', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_branches(self, **kwargs):
        """Get all branches."""
        branches = request.env['education.branch'].sudo().search(
            [('active', '=', True)])
        return json_response({
            'branches': [{
                'id': b.id,
                'name': b.name,
                'code': b.code,
                'address': b.address or '',
                'phone': b.phone or '',
                'is_main': b.is_main,
            } for b in branches],
        })
