import json
import logging
import functools
from datetime import datetime, timedelta

import jwt

from odoo import http, fields
from odoo.http import request, Response

_logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET_KEY = 'dar-alanwar-jwt-secret-key-change-in-production'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = 24


def json_response(data, status=200):
    """Return a JSON response."""
    return Response(
        json.dumps(data, default=str),
        status=status,
        content_type='application/json',
    )


def error_response(message, status=400, code=None):
    """Return an error JSON response."""
    body = {'error': True, 'message': message}
    if code:
        body['code'] = code
    return json_response(body, status=status)


def generate_jwt_token(parent_id, email):
    """Generate a JWT token for a parent."""
    payload = {
        'parent_id': parent_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(func):
    """Decorator that requires a valid JWT token."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error_response('Missing or invalid Authorization header', 401,
                                  'AUTH_REQUIRED')

        token = auth_header[7:]
        payload = decode_jwt_token(token)
        if not payload:
            return error_response('Invalid or expired token', 401,
                                  'TOKEN_INVALID')

        parent = request.env['res.partner'].sudo().browse(
            payload.get('parent_id'))
        if not parent.exists() or not parent.is_guardian:
            return error_response('Parent not found', 401, 'PARENT_NOT_FOUND')

        request.parent = parent
        return func(*args, **kwargs)
    return wrapper


def get_request_data():
    """Parse JSON data from request body."""
    try:
        if request.httprequest.content_type == 'application/json':
            return json.loads(request.httprequest.data)
        return {}
    except (json.JSONDecodeError, Exception):
        return {}


class ApiBaseController(http.Controller):
    """Base controller for API endpoints."""

    def _get_parent_children(self, parent):
        """Get all children for a parent."""
        children = parent.father_student_ids | parent.mother_student_ids
        return children.filtered(lambda s: s.student_state in ('enrolled', 'suspended'))

    def _serialize_student(self, student):
        """Serialize a student record to dict."""
        return {
            'id': student.id,
            'code': student.code,
            'name': student.name,
            'arabic_name': student.arabic_name or '',
            'birthdate': str(student.birthdate) if student.birthdate else None,
            'gender': student.gender,
            'photo_url': f'/web/image/res.partner/{student.id}/image_1920'
            if student.image_1920 else None,
            'department': {
                'id': student.department_id.id,
                'name': student.department_id.name,
            } if student.department_id else None,
            'class': {
                'id': student.class_id.id,
                'name': student.class_id.name,
            } if student.class_id else None,
            'level': {
                'id': student.level_id.id,
                'name': student.level_id.name,
            } if student.level_id else None,
            'state': student.student_state,
            'balance_due': student.balance_due,
            'attendance_rate': student.attendance_rate,
            'enrollment_date': str(student.enrollment_date)
            if student.enrollment_date else None,
        }

    def _serialize_installment(self, inst):
        """Serialize an installment record."""
        return {
            'id': inst.id,
            'sequence': inst.sequence,
            'due_date': str(inst.due_date),
            'amount': inst.amount,
            'paid_amount': inst.paid_amount,
            'is_paid': inst.is_paid,
        }

    def _serialize_payment(self, payment):
        """Serialize a payment record."""
        return {
            'id': payment.id,
            'date': str(payment.date),
            'amount': payment.amount,
            'payment_method': payment.payment_method,
            'reference': payment.reference or '',
        }

    def _serialize_attendance(self, line):
        """Serialize an attendance line."""
        return {
            'id': line.id,
            'date': str(line.attendance_id.date),
            'status': line.status,
            'check_in_time': str(line.check_in_time) if line.check_in_time else None,
            'check_out_time': str(line.check_out_time) if line.check_out_time else None,
            'hours_present': line.hours_present,
            'late_minutes': line.late_minutes,
            'class': line.attendance_id.class_id.name
            if line.attendance_id.class_id else '',
        }
