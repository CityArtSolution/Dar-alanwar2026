import logging

from odoo import http
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response, jwt_required,
)

_logger = logging.getLogger(__name__)


class SubscriptionsApiController(ApiBaseController):

    @http.route('/api/subscriptions', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_subscriptions(self, **kwargs):
        """Get subscriptions for parent's children."""
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

        subs = request.env['education.student.subscription'].sudo().search(domain)

        return json_response({
            'subscriptions': [{
                'id': s.id,
                'student_id': s.student_id.id,
                'student_name': s.student_id.name,
                'type': s.type_id.name if s.type_id else '',
                'total_amount': s.total_amount,
                'discount_amount': s.discount_amount,
                'net_amount': s.net_amount,
                'paid_amount': s.paid_amount,
                'remaining_amount': s.remaining_amount,
                'status': s.status,
                'installments': [
                    self._serialize_installment(i) for i in s.installment_ids
                ],
            } for s in subs],
        })

    @http.route('/api/subscriptions/<int:sub_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @jwt_required
    def get_subscription_detail(self, sub_id, **kwargs):
        """Get subscription detail with installments."""
        parent = request.parent
        children = self._get_parent_children(parent)

        sub = request.env['education.student.subscription'].sudo().browse(sub_id)
        if not sub.exists() or sub.student_id.id not in children.ids:
            return error_response('Subscription not found', 404)

        # Get payments for each installment
        installments = []
        for inst in sub.installment_ids:
            inst_data = self._serialize_installment(inst)
            inst_data['payments'] = [
                self._serialize_payment(p) for p in inst.payment_ids
            ]
            installments.append(inst_data)

        return json_response({
            'id': sub.id,
            'student': self._serialize_student(sub.student_id),
            'type': sub.type_id.name if sub.type_id else '',
            'plan': sub.plan_id.name if sub.plan_id else '',
            'total_amount': sub.total_amount,
            'discount': {
                'name': sub.discount_id.name if sub.discount_id else None,
                'type': sub.discount_type,
                'amount': sub.discount_amount,
            },
            'net_amount': sub.net_amount,
            'paid_amount': sub.paid_amount,
            'remaining_amount': sub.remaining_amount,
            'status': sub.status,
            'installments': installments,
        })
