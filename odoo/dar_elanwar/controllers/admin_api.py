import logging
from datetime import date

from odoo import http, fields
from odoo.http import request

from .api_base import (
    ApiBaseController, json_response, error_response,
    admin_jwt_required, get_request_data,
)

_logger = logging.getLogger(__name__)

PAGE_SIZE = 20


class AdminApiController(ApiBaseController):

    # ─── Dashboard ────────────────────────────────────────────

    @http.route('/api/admin/dashboard', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_dashboard(self, **kwargs):
        """Return dashboard statistics."""
        env = request.env

        # Counts
        student_count = env['res.partner'].sudo().search_count(
            [('is_student', '=', True)])
        parent_count = env['res.partner'].sudo().search_count(
            [('is_guardian', '=', True)])
        teacher_count = env['education.employee'].sudo().search_count(
            [('is_teacher', '=', True), ('state', '=', 'active')])

        # Subscriptions
        Sub = env['education.student.subscription'].sudo()
        active_subs = Sub.search_count([('status', '=', 'active')])
        draft_subs = Sub.search_count([('status', '=', 'draft')])
        expired_subs = Sub.search_count([('status', '=', 'expired')])

        # Revenue — sum of paid invoices linked to subscriptions
        Invoice = env['account.move'].sudo()
        paid_invoices = Invoice.search([
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '=', 'paid'),
        ])
        total_revenue = sum(paid_invoices.mapped('amount_total'))

        # Invoice stats
        all_invoices = Invoice.search([('move_type', '=', 'out_invoice')])
        invoice_paid = len(all_invoices.filtered(
            lambda i: i.payment_state == 'paid'))
        invoice_pending = len(all_invoices.filtered(
            lambda i: i.state == 'posted' and i.payment_state != 'paid'
            and (not i.invoice_date_due or i.invoice_date_due >= date.today())))
        invoice_draft = len(all_invoices.filtered(
            lambda i: i.state == 'draft'))
        invoice_overdue = len(all_invoices.filtered(
            lambda i: i.state == 'posted' and i.payment_state != 'paid'
            and i.invoice_date_due and i.invoice_date_due < date.today()))

        # Attendance today
        today = fields.Date.today()
        AttLine = env['education.attendance.line'].sudo()
        today_attendance = AttLine.search([
            ('attendance_id.date', '=', today),
        ])
        today_present = len(today_attendance.filtered(
            lambda l: l.status in ('present', 'late')))
        today_total = len(today_attendance) if today_attendance else student_count
        attendance_rate = round(
            (today_present / today_total * 100) if today_total else 0, 1)

        # Recent students (last 10)
        recent = env['res.partner'].sudo().search(
            [('is_student', '=', True)],
            order='create_date desc', limit=10)
        recent_students = []
        for s in recent:
            recent_students.append({
                'id': s.id,
                'name': s.name,
                'department': s.department_id.name if s.department_id else '',
                'class_name': s.class_id.name if s.class_id else '',
                'state': s.student_state,
                'date': str(s.create_date.date()) if s.create_date else '',
            })

        # Today summary
        today_invoices = Invoice.search([
            ('move_type', '=', 'out_invoice'),
            ('create_date', '>=', str(today) + ' 00:00:00'),
            ('create_date', '<=', str(today) + ' 23:59:59'),
        ])
        new_students_today = env['res.partner'].sudo().search_count([
            ('is_student', '=', True),
            ('create_date', '>=', str(today) + ' 00:00:00'),
            ('create_date', '<=', str(today) + ' 23:59:59'),
        ])

        return json_response({
            'student_count': student_count,
            'parent_count': parent_count,
            'teacher_count': teacher_count,
            'active_subscriptions': active_subs,
            'total_revenue': total_revenue,
            'attendance_rate': attendance_rate,
            'subscription_stats': {
                'active': active_subs,
                'draft': draft_subs,
                'expired': expired_subs,
            },
            'invoice_stats': {
                'paid': invoice_paid,
                'pending': invoice_pending,
                'draft': invoice_draft,
                'overdue': invoice_overdue,
            },
            'recent_students': recent_students,
            'today_summary': {
                'present': today_present,
                'total': today_total,
                'invoices': len(today_invoices),
                'invoice_total': sum(today_invoices.mapped('amount_total')),
                'new_students': new_students_today,
            },
        })

    # ─── Students ─────────────────────────────────────────────

    @http.route('/api/admin/students', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_students(self, **kwargs):
        """Paginated student list with search/filters."""
        params = request.params
        search = params.get('search', '').strip()
        department = params.get('department', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = [('is_student', '=', True)]
        if search:
            domain += ['|', '|',
                        ('name', 'ilike', search),
                        ('arabic_name', 'ilike', search),
                        ('code', 'ilike', search)]
        if department:
            domain.append(('department_id.name', 'ilike', department))
        if status:
            domain.append(('student_state', '=', status))

        Student = request.env['res.partner'].sudo()
        total = Student.search_count(domain)
        students = Student.search(domain, order='create_date desc',
                                  limit=limit, offset=offset)

        result = []
        for s in students:
            # Find parent
            parent_name = ''
            if s.father_id:
                parent_name = s.father_id.name
            elif s.mother_id:
                parent_name = s.mother_id.name

            result.append({
                'id': s.id,
                'name': s.name,
                'arabic_name': s.arabic_name or '',
                'code': s.code or '',
                'department': s.department_id.name if s.department_id else '',
                'class_name': s.class_id.name if s.class_id else '',
                'parent_name': parent_name,
                'state': s.student_state,
                'attendance': s.attendance_rate or 0,
                'enrollment_date': str(s.enrollment_date) if s.enrollment_date else '',
            })

        return json_response({
            'students': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Parents ──────────────────────────────────────────────

    @http.route('/api/admin/parents', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_parents(self, **kwargs):
        """Paginated parent list."""
        params = request.params
        search = params.get('search', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = [('is_guardian', '=', True)]
        if search:
            domain += ['|', '|',
                        ('name', 'ilike', search),
                        ('phone', 'ilike', search),
                        ('email', 'ilike', search)]

        Parent = request.env['res.partner'].sudo()
        total = Parent.search_count(domain)
        parents = Parent.search(domain, order='create_date desc',
                                limit=limit, offset=offset)

        result = []
        for p in parents:
            result.append({
                'id': p.id,
                'name': p.name,
                'phone': p.phone or '',
                'email': p.email or '',
                'children_count': p.children_count,
                'children_balance_due': p.children_balance_due,
                'guardian_relation': p.guardian_relation or '',
            })

        return json_response({
            'parents': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Subscriptions ────────────────────────────────────────

    @http.route('/api/admin/subscriptions', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_subscriptions(self, **kwargs):
        """Paginated subscription list."""
        params = request.params
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = []
        if search:
            domain += ['|',
                        ('student_id.name', 'ilike', search),
                        ('subscription_type_id.name', 'ilike', search)]
        if status:
            domain.append(('status', '=', status))

        Sub = request.env['education.student.subscription'].sudo()
        total = Sub.search_count(domain)
        subs = Sub.search(domain, order='create_date desc',
                          limit=limit, offset=offset)

        result = []
        for s in subs:
            result.append({
                'id': s.id,
                'student': s.student_id.name if s.student_id else '',
                'student_id': s.student_id.id if s.student_id else None,
                'type': s.subscription_type_id.name if s.subscription_type_id else '',
                'status': s.status,
                'start_date': str(s.start_date) if s.start_date else '',
                'end_date': str(s.end_date) if s.end_date else '',
                'total_amount': s.total_amount,
                'paid_amount': s.paid_amount,
                'remaining_amount': s.remaining_amount,
            })

        return json_response({
            'subscriptions': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Invoices ─────────────────────────────────────────────

    @http.route('/api/admin/invoices', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_invoices(self, **kwargs):
        """Paginated invoice list."""
        params = request.params
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = [('move_type', '=', 'out_invoice')]
        if search:
            domain += ['|',
                        ('partner_id.name', 'ilike', search),
                        ('name', 'ilike', search)]
        if status == 'paid':
            domain.append(('payment_state', '=', 'paid'))
        elif status == 'draft':
            domain.append(('state', '=', 'draft'))
        elif status == 'overdue':
            domain += [
                ('state', '=', 'posted'),
                ('payment_state', '!=', 'paid'),
                ('invoice_date_due', '<', str(date.today())),
            ]
        elif status == 'pending':
            domain += [
                ('state', '=', 'posted'),
                ('payment_state', '!=', 'paid'),
                '|',
                ('invoice_date_due', '=', False),
                ('invoice_date_due', '>=', str(date.today())),
            ]

        Invoice = request.env['account.move'].sudo()
        total = Invoice.search_count(domain)
        invoices = Invoice.search(domain, order='create_date desc',
                                  limit=limit, offset=offset)

        result = []
        for inv in invoices:
            result.append({
                'id': inv.id,
                'name': inv.name or '',
                'partner': inv.partner_id.name if inv.partner_id else '',
                'date': str(inv.invoice_date) if inv.invoice_date else '',
                'due_date': str(inv.invoice_date_due) if inv.invoice_date_due else '',
                'amount': inv.amount_total,
                'paid_amount': inv.amount_total - inv.amount_residual,
                'residual': inv.amount_residual,
                'state': inv.state,
                'payment_state': inv.payment_state or '',
            })

        return json_response({
            'invoices': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })
