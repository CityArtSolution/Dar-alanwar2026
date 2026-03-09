import logging

from odoo import http, fields
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class ContentApiController(ApiBaseController):

    @http.route('/api/content/categories', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_categories(self, **kwargs):
        """Get content categories."""
        categories = request.env['education.content.category'].sudo().search(
            [('active', '=', True)])

        return json_response({
            'categories': [{
                'id': c.id,
                'name': c.name,
                'code': c.code,
                'content_type': c.content_type,
                'icon': c.icon or '',
                'item_count': c.item_count,
            } for c in categories],
        })

    @http.route('/api/content/items', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_content_items(self, **kwargs):
        """Get content items accessible to parent's children."""
        parent = request.parent
        children = self._get_parent_children(parent)

        student_id = kwargs.get('student_id')
        category_id = kwargs.get('category_id')
        content_type = kwargs.get('type')

        domain = [
            ('student_id', 'in', children.ids),
            ('is_active', '=', True),
        ]

        if student_id:
            student_id = int(student_id)
            if student_id not in children.ids:
                return error_response('Student not found', 404)
            domain = [('student_id', '=', student_id), ('is_active', '=', True)]

        access_records = request.env['education.content.access'].sudo().search(domain)
        item_ids = access_records.mapped('content_item_id').ids

        item_domain = [('id', 'in', item_ids), ('active', '=', True)]
        if category_id:
            item_domain.append(('category_id', '=', int(category_id)))
        if content_type:
            item_domain.append(('content_type', '=', content_type))

        items = request.env['education.content.item'].sudo().search(item_domain)

        return json_response({
            'items': [{
                'id': item.id,
                'name': item.name,
                'category': item.category_id.name if item.category_id else '',
                'content_type': item.content_type,
                'description': item.description or '',
                'file_url': item.file_url or '',
                'thumbnail_url': f'/web/image/education.content.item/{item.id}/thumbnail'
                if item.thumbnail else None,
                'is_drm_protected': item.is_drm_protected,
                'target_age_min': item.target_age_min,
                'target_age_max': item.target_age_max,
            } for item in items],
        })

    @http.route('/api/content/items/<int:item_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_content_detail(self, item_id, **kwargs):
        """Get content item detail."""
        parent = request.parent
        children = self._get_parent_children(parent)

        # Verify access
        access = request.env['education.content.access'].sudo().search([
            ('content_item_id', '=', item_id),
            ('student_id', 'in', children.ids),
            ('is_active', '=', True),
        ], limit=1)

        if not access:
            return error_response('Content not accessible', 403)

        item = request.env['education.content.item'].sudo().browse(item_id)
        if not item.exists():
            return error_response('Content not found', 404)

        # Log usage
        student_id = kwargs.get('student_id', children[0].id if children else False)
        request.env['education.content.usage'].sudo().create({
            'student_id': int(student_id),
            'content_item_id': item.id,
        })

        return json_response({
            'id': item.id,
            'name': item.name,
            'category': item.category_id.name if item.category_id else '',
            'content_type': item.content_type,
            'description': item.description or '',
            'file_url': item.file_url or '',
            'is_drm_protected': item.is_drm_protected,
            'grade_levels': [l.name for l in item.grade_level_ids],
        })
