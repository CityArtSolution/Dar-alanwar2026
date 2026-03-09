import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class AttendanceApiController(ApiBaseController):

    @http.route('/api/attendance/<int:student_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_student_attendance(self, student_id, **kwargs):
        """Get attendance records for a student."""
        parent = request.parent
        children = self._get_parent_children(parent)
        student = children.filtered(lambda s: s.id == student_id)

        if not student:
            return error_response('Student not found', 404)

        # Optional filters
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        limit = int(kwargs.get('limit', 50))
        offset = int(kwargs.get('offset', 0))

        domain = [('student_id', '=', student_id)]
        if date_from:
            domain.append(('attendance_id.date', '>=', date_from))
        if date_to:
            domain.append(('attendance_id.date', '<=', date_to))

        lines = request.env['education.attendance.line'].sudo().search(
            domain, order='attendance_id desc', limit=limit, offset=offset)

        total = request.env['education.attendance.line'].sudo().search_count(domain)

        return json_response({
            'student_id': student_id,
            'attendance_rate': student[0].attendance_rate,
            'total': total,
            'records': [self._serialize_attendance(line) for line in lines],
        })

    @http.route('/api/attendance/<int:student_id>/summary', type='http',
                auth='none', methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_attendance_summary(self, student_id, **kwargs):
        """Get attendance summary for a student."""
        parent = request.parent
        children = self._get_parent_children(parent)
        student = children.filtered(lambda s: s.id == student_id)

        if not student:
            return error_response('Student not found', 404)

        lines = request.env['education.attendance.line'].sudo().search(
            [('student_id', '=', student_id)])

        total = len(lines)
        present = len(lines.filtered(lambda l: l.status == 'present'))
        absent = len(lines.filtered(lambda l: l.status == 'absent'))
        late = len(lines.filtered(lambda l: l.status == 'late'))
        excused = len(lines.filtered(lambda l: l.status == 'excused'))

        return json_response({
            'student_id': student_id,
            'total_days': total,
            'present': present,
            'absent': absent,
            'late': late,
            'excused': excused,
            'attendance_rate': (present + late) / total * 100 if total else 0,
        })
