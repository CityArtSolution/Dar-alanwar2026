import logging

from odoo import http, fields
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    jwt_required, get_request_data,
)

_logger = logging.getLogger(__name__)


class PaymentsApiController(ApiBaseController):

    @http.route('/api/payments', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_payments(self, **kwargs):
        """Get payment history for parent's children."""
        parent = request.parent
        children = self._get_parent_children(parent)

        student_id = kwargs.get('student_id')
        if student_id:
            student_id = int(student_id)
            if student_id not in children.ids:
                return error_response('Student not found', 404)
            domain = [('student_id', '=', student_id)]
        else:
            domain = [('student_id', 'in', children.ids)]

        payments = request.env['education.payment'].sudo().search(
            domain, order='date desc', limit=int(kwargs.get('limit', 50)))

        return json_response({
            'payments': [self._serialize_payment(p) for p in payments],
        })

    @http.route('/api/payments', type='http', auth='none',
                methods=['POST'], csrf=False, cors='*')
    @jwt_required
    def create_payment(self, **kwargs):
        """Record a payment (online payment confirmation)."""
        parent = request.parent
        children = self._get_parent_children(parent)
        data = get_request_data()

        installment_id = data.get('installment_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method', 'online')
        reference = data.get('reference', '')

        if not installment_id or not amount:
            return error_response('installment_id and amount are required')

        installment = request.env['education.installment'].sudo().browse(
            int(installment_id))
        if not installment.exists():
            return error_response('Installment not found', 404)

        if installment.student_id.id not in children.ids:
            return error_response('Unauthorized', 403)

        if installment.is_paid:
            return error_response('Installment already paid')

        payment = request.env['education.payment'].sudo().create({
            'installment_id': installment.id,
            'date': fields.Date.today(),
            'amount': float(amount),
            'payment_method': payment_method,
            'reference': reference,
        })

        return json_response({
            'success': True,
            'payment': self._serialize_payment(payment),
            'installment': self._serialize_installment(installment),
        }, status=201)

    @http.route('/api/payments/balance', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_balance(self, **kwargs):
        """Get total balance due for parent's children."""
        parent = request.parent
        children = self._get_parent_children(parent)

        balances = []
        for child in children:
            balances.append({
                'student_id': child.id,
                'student_name': child.name,
                'balance_due': child.balance_due,
            })

        return json_response({
            'total_balance': sum(b['balance_due'] for b in balances),
            'children': balances,
        })
