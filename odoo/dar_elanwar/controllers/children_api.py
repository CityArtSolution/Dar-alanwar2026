import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class ChildrenApiController(ApiBaseController):

    @http.route('/api/children', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_children(self, **kwargs):
        """Get all children for the authenticated parent."""
        parent = request.parent
        children = self._get_parent_children(parent)
        return json_response({
            'children': [self._serialize_student(c) for c in children],
        })

    @http.route('/api/children/<int:student_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_child_detail(self, student_id, **kwargs):
        """Get detailed info for a specific child."""
        parent = request.parent
        children = self._get_parent_children(parent)
        student = children.filtered(lambda s: s.id == student_id)

        if not student:
            return error_response('Student not found', 404)

        student = student[0]
        data = self._serialize_student(student)

        # Add detailed info
        data['medical'] = {
            'blood_type': student.blood_type,
            'allergies': student.allergies or '',
            'medical_notes': student.medical_notes or '',
        }

        # Goals
        evaluations = request.env['education.student.evaluation'].sudo().search(
            [('student_id', '=', student.id)])
        data['goals'] = [{
            'id': ev.id,
            'name': ev.goal_id.name,
            'state': ev.goal_id.state,
            'is_completed': ev.is_completed,
        } for ev in evaluations[:20]]

        # Homework
        submissions = request.env['education.homework.submission'].sudo().search(
            [('student_id', '=', student.id)], order='submit_date desc', limit=20)
        data['homework'] = [{
            'id': sub.id,
            'title': sub.homework_id.name,
            'due_date': str(sub.homework_id.due_date),
            'is_graded': sub.is_graded,
            'grade': sub.grade,
        } for sub in submissions]

        return json_response(data)

    @http.route('/api/children/<int:student_id>/siblings', type='http',
                auth='none', methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_child_siblings(self, student_id, **kwargs):
        """Get siblings of a student."""
        parent = request.parent
        children = self._get_parent_children(parent)
        student = children.filtered(lambda s: s.id == student_id)

        if not student:
            return error_response('Student not found', 404)

        siblings = student[0].sibling_ids
        return json_response({
            'siblings': [{
                'id': s.id,
                'name': s.name,
                'birthdate': str(s.birthdate) if s.birthdate else None,
                'gender': s.gender,
                'is_enrolled': s.is_enrolled,
            } for s in siblings],
        })
