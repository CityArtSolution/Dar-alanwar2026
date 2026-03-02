import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class InvoicesApiController(ApiBaseController):

    @http.route('/api/invoices', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_invoices(self, **kwargs):
        """Get all invoices/receipts for parent's children."""
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

        receipts = request.env['education.payment.receipt'].sudo().search(
            domain, order='date desc')

        return json_response({
            'invoices': [{
                'id': r.id,
                'receipt_number': r.receipt_number,
                'student_id': r.student_id.id,
                'student_name': r.student_id.name,
                'date': str(r.date),
                'total_amount': r.total_amount,
            } for r in receipts],
        })

    @http.route('/api/invoices/<int:receipt_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_invoice_detail(self, receipt_id, **kwargs):
        """Get invoice detail."""
        parent = request.parent
        children = self._get_parent_children(parent)

        receipt = request.env['education.payment.receipt'].sudo().browse(receipt_id)
        if not receipt.exists() or receipt.student_id.id not in children.ids:
            return error_response('Invoice not found', 404)

        return json_response({
            'id': receipt.id,
            'receipt_number': receipt.receipt_number,
            'student': self._serialize_student(receipt.student_id),
            'date': str(receipt.date),
            'total_amount': receipt.total_amount,
            'notes': receipt.notes or '',
        })
