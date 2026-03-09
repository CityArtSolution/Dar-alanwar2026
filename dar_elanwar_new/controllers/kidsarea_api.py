import logging

from odoo import http, fields
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    jwt_required, get_request_data,
)

_logger = logging.getLogger(__name__)


class KidsAreaApiController(ApiBaseController):

    @http.route('/api/kidsarea/services', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_services(self, **kwargs):
        """Get available kids area services."""
        services = request.env['education.kids.area.service'].sudo().search(
            [('active', '=', True)])

        return json_response({
            'services': [{
                'id': s.id,
                'name': s.name,
                'activity_type': s.activity_type,
                'pricing_type': s.pricing_type,
                'price': s.price,
                'capacity': s.capacity,
                'min_age': s.min_age,
                'max_age': s.max_age,
                'duration_minutes': s.duration_minutes,
                'description': s.description or '',
                'image_url': f'/web/image/education.kids.area.service/{s.id}/image'
                if s.image else None,
            } for s in services],
        })

    @http.route('/api/kidsarea/slots', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_available_slots(self, **kwargs):
        """Get available time slots."""
        service_id = kwargs.get('service_id')
        date = kwargs.get('date')

        domain = [('state', '=', 'available')]
        if service_id:
            domain.append(('service_id', '=', int(service_id)))
        if date:
            domain.append(('date', '=', date))
        else:
            domain.append(('date', '>=', fields.Date.today()))

        slots = request.env['education.kids.area.slot'].sudo().search(
            domain, order='date, time_from', limit=50)

        return json_response({
            'slots': [{
                'id': sl.id,
                'service': sl.service_id.name,
                'service_id': sl.service_id.id,
                'date': str(sl.date),
                'time_from': sl.time_from,
                'time_to': sl.time_to,
                'available_count': sl.available_count,
                'state': sl.state,
                'price': sl.service_id.price,
            } for sl in slots],
        })

    @http.route('/api/kidsarea/bookings', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_bookings(self, **kwargs):
        """Get parent's bookings."""
        parent = request.parent
        bookings = request.env['education.kids.area.booking'].sudo().search(
            [('parent_id', '=', parent.id)], order='booking_date desc')

        return json_response({
            'bookings': [{
                'id': b.id,
                'service': b.slot_id.service_id.name,
                'date': str(b.slot_id.date),
                'time_from': b.slot_id.time_from,
                'time_to': b.slot_id.time_to,
                'student': b.student_id.name,
                'state': b.state,
                'amount': b.amount,
                'payment_status': b.payment_status,
                'qr_code': b.qr_code,
            } for b in bookings],
        })

    @http.route('/api/kidsarea/bookings', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def create_booking(self, **kwargs):
        """Create a new booking."""
        parent = request.parent
        children = self._get_parent_children(parent)
        data = get_request_data()

        slot_id = data.get('slot_id')
        student_id = data.get('student_id')

        if not slot_id or not student_id:
            return error_response('slot_id and student_id are required')

        student_id = int(student_id)
        if student_id not in children.ids:
            return error_response('Student not found', 404)

        slot = request.env['education.kids.area.slot'].sudo().browse(int(slot_id))
        if not slot.exists():
            return error_response('Slot not found', 404)

        if slot.state == 'full':
            return error_response('This slot is full')

        if slot.state == 'closed':
            return error_response('This slot is closed')

        booking = request.env['education.kids.area.booking'].sudo().create({
            'slot_id': slot.id,
            'student_id': student_id,
            'parent_id': parent.id,
        })
        booking.action_confirm()

        return json_response({
            'success': True,
            'booking': {
                'id': booking.id,
                'qr_code': booking.qr_code,
                'state': booking.state,
                'amount': booking.amount,
            },
        }, status=201)

    @http.route('/api/kidsarea/bookings/<int:booking_id>/cancel', type='http',
                auth='none', methods=['DELETE'], csrf=False, cors='*')
    @jwt_required
    def cancel_booking(self, booking_id, **kwargs):
        """Cancel a booking."""
        parent = request.parent
        booking = request.env['education.kids.area.booking'].sudo().browse(
            booking_id)

        if not booking.exists() or booking.parent_id.id != parent.id:
            return error_response('Booking not found', 404)

        if booking.state not in ('draft', 'confirmed'):
            return error_response('Cannot cancel this booking')

        booking.action_cancel()
        return json_response({'success': True, 'message': 'Booking cancelled'})

    @http.route('/api/kidsarea/packages', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_packages(self, **kwargs):
        """Get available packages."""
        packages = request.env['education.kids.area.package'].sudo().search(
            [('active', '=', True)])

        return json_response({
            'packages': [{
                'id': p.id,
                'name': p.name,
                'services': [s.name for s in p.service_ids],
                'session_count': p.session_count,
                'price': p.price,
                'validity_days': p.validity_days,
                'description': p.description or '',
            } for p in packages],
        })
