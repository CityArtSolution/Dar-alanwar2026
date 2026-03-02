import logging

from odoo import http, fields
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    jwt_required, get_request_data,
)

_logger = logging.getLogger(__name__)


class MessagesApiController(ApiBaseController):

    @http.route('/api/messages', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_messages(self, **kwargs):
        """Get messages and announcements for parent."""
        parent = request.parent
        children = self._get_parent_children(parent)

        # Personal messages
        messages = request.env['education.message'].sudo().search(
            [('parent_id', '=', parent.id)], order='date desc',
            limit=int(kwargs.get('limit', 30)))

        # Announcements
        dept_ids = children.mapped('department_id').ids
        class_ids = children.mapped('class_id').ids

        ann_domain = [
            ('is_published', '=', True),
            '|', '|', '|',
            ('target_type', '=', 'all'),
            ('target_type', '=', 'parents'),
            '&', ('target_type', '=', 'department'),
            ('department_id', 'in', dept_ids),
            '&', ('target_type', '=', 'class'),
            ('class_id', 'in', class_ids),
        ]

        announcements = request.env['education.announcement'].sudo().search(
            ann_domain, order='date desc', limit=20)

        return json_response({
            'messages': [{
                'id': m.id,
                'type': 'message',
                'subject': m.subject,
                'body': m.body or '',
                'date': str(m.date),
                'is_read': m.is_read,
                'sender': m.sender_id.name if m.sender_id else 'System',
            } for m in messages],
            'announcements': [{
                'id': a.id,
                'type': 'announcement',
                'title': a.title,
                'content': a.content or '',
                'date': str(a.date),
                'priority': a.priority,
                'target_type': a.target_type,
            } for a in announcements],
        })

    @http.route('/api/messages', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def send_message(self, **kwargs):
        """Send a message or support ticket from parent."""
        parent = request.parent
        data = get_request_data()

        subject = data.get('subject', '')
        body = data.get('body', '')
        message_type = data.get('type', 'message')

        if not subject or not body:
            return error_response('Subject and body are required')

        if message_type == 'ticket':
            ticket = request.env['education.support.ticket'].sudo().create({
                'subject': subject,
                'description': body,
                'parent_id': parent.id,
                'category': data.get('category', 'other'),
            })
            return json_response({
                'success': True,
                'ticket': {
                    'id': ticket.id,
                    'name': ticket.name,
                    'subject': ticket.subject,
                    'state': ticket.state,
                },
            }, status=201)
        else:
            msg = request.env['education.message'].sudo().create({
                'subject': subject,
                'body': body,
                'recipient_type': 'user',
                'sender_id': False,
            })
            return json_response({
                'success': True,
                'message_id': msg.id,
            }, status=201)

    @http.route('/api/messages/<int:message_id>/read', type='http',
                auth='none', methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def mark_read(self, message_id, **kwargs):
        """Mark a message as read."""
        parent = request.parent
        msg = request.env['education.message'].sudo().browse(message_id)

        if not msg.exists() or msg.parent_id.id != parent.id:
            return error_response('Message not found', 404)

        msg.action_mark_read()
        return json_response({'success': True})

    @http.route('/api/messages/unread-count', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def unread_count(self, **kwargs):
        """Get unread message count."""
        parent = request.parent
        count = request.env['education.message'].sudo().search_count(
            [('parent_id', '=', parent.id), ('is_read', '=', False)])
        return json_response({'unread_count': count})
