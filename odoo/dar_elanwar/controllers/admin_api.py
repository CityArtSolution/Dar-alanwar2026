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

    # ─── Teachers ────────────────────────────────────────────

    @http.route('/api/admin/teachers', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_teachers(self, **kwargs):
        """Paginated teacher list."""
        params = request.params
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = [('is_teacher', '=', True)]
        if search:
            domain += ['|', '|',
                        ('name', 'ilike', search),
                        ('code', 'ilike', search),
                        ('phone', 'ilike', search)]
        if status:
            domain.append(('state', '=', status))

        Teacher = request.env['education.employee'].sudo()
        total = Teacher.search_count(domain)
        teachers = Teacher.search(domain, order='create_date desc',
                                  limit=limit, offset=offset)

        result = []
        for t in teachers:
            result.append({
                'id': t.id,
                'code': t.code or '',
                'name': t.name or '',
                'phone': t.phone or t.mobile or '',
                'email': t.email or '',
                'job_title': t.job_title or '',
                'department': t.department_id.name if t.department_id else '',
                'shift_type': t.shift_type or '',
                'state': t.state,
                'hire_date': str(t.hire_date) if t.hire_date else '',
                'class_count': t.class_count if hasattr(t, 'class_count') else 0,
            })

        return json_response({
            'teachers': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Attendance ──────────────────────────────────────────

    @http.route('/api/admin/attendance', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_attendance(self, **kwargs):
        """Paginated attendance records."""
        params = request.params
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        date_from = params.get('date_from', '').strip()
        date_to = params.get('date_to', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = []
        if search:
            domain += ['|',
                        ('class_id.name', 'ilike', search),
                        ('department_id.name', 'ilike', search)]
        if status:
            domain.append(('state', '=', status))
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))

        Att = request.env['education.attendance'].sudo()
        total = Att.search_count(domain)
        records = Att.search(domain, order='date desc',
                             limit=limit, offset=offset)

        result = []
        for a in records:
            result.append({
                'id': a.id,
                'date': str(a.date) if a.date else '',
                'department': a.department_id.name if a.department_id else '',
                'class_name': a.class_id.name if a.class_id else '',
                'state': a.state,
                'present_count': a.present_count,
                'absent_count': a.absent_count,
                'late_count': a.late_count,
                'total_count': a.total_count,
                'recorded_by': a.recorded_by.name if a.recorded_by else '',
            })

        return json_response({
            'attendance': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Content ─────────────────────────────────────────────

    @http.route('/api/admin/content', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_content(self, **kwargs):
        """Paginated content library."""
        params = request.params
        search = params.get('search', '').strip()
        content_type = params.get('type', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = []
        if search:
            domain += [('name', 'ilike', search)]
        if content_type:
            domain.append(('content_type', '=', content_type))

        Content = request.env['education.content.item'].sudo()
        total = Content.search_count(domain)
        items = Content.search(domain, order='create_date desc',
                               limit=limit, offset=offset)

        result = []
        for c in items:
            result.append({
                'id': c.id,
                'name': c.name or '',
                'category': c.category_id.name if c.category_id else '',
                'content_type': c.content_type or '',
                'target_age_min': c.target_age_min,
                'target_age_max': c.target_age_max,
                'access_count': c.access_count if hasattr(c, 'access_count') else 0,
                'active': c.active,
                'has_file': bool(c.file_url or c.file),
            })

        return json_response({
            'content': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Kids Area ───────────────────────────────────────────

    @http.route('/api/admin/kidsarea', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_kidsarea(self, **kwargs):
        """Kids area services and bookings."""
        params = request.params
        view = params.get('view', 'services').strip()
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        if view == 'bookings':
            domain = []
            if search:
                domain += ['|',
                            ('student_id.name', 'ilike', search),
                            ('parent_id.name', 'ilike', search)]
            if status:
                domain.append(('state', '=', status))

            Booking = request.env['education.kids.area.booking'].sudo()
            total = Booking.search_count(domain)
            bookings = Booking.search(domain, order='booking_date desc',
                                      limit=limit, offset=offset)

            result = []
            for b in bookings:
                service_name = ''
                if b.slot_id and b.slot_id.service_id:
                    service_name = b.slot_id.service_id.name
                result.append({
                    'id': b.id,
                    'student': b.student_id.name if b.student_id else '',
                    'parent': b.parent_id.name if b.parent_id else '',
                    'service': service_name,
                    'booking_date': str(b.booking_date) if b.booking_date else '',
                    'state': b.state,
                    'amount': b.amount,
                    'payment_status': b.payment_status or '',
                })

            return json_response({
                'bookings': result,
                'total': total,
                'page': page,
                'pages': (total + limit - 1) // limit if limit else 1,
            })
        else:
            domain = []
            if search:
                domain += [('name', 'ilike', search)]

            Service = request.env['education.kids.area.service'].sudo()
            total = Service.search_count(domain)
            services = Service.search(domain, order='name',
                                      limit=limit, offset=offset)

            result = []
            for s in services:
                result.append({
                    'id': s.id,
                    'name': s.name or '',
                    'activity_type': s.activity_type or '',
                    'pricing_type': s.pricing_type or '',
                    'price': s.price,
                    'capacity': s.capacity,
                    'min_age': s.min_age,
                    'max_age': s.max_age,
                    'duration_minutes': s.duration_minutes,
                    'active': s.active,
                })

            return json_response({
                'services': result,
                'total': total,
                'page': page,
                'pages': (total + limit - 1) // limit if limit else 1,
            })

    # ─── Messages ────────────────────────────────────────────

    @http.route('/api/admin/messages', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_messages(self, **kwargs):
        """Paginated messages list."""
        params = request.params
        search = params.get('search', '').strip()
        status = params.get('status', '').strip()
        page = int(params.get('page', 1))
        limit = int(params.get('limit', PAGE_SIZE))
        offset = (page - 1) * limit

        domain = []
        if search:
            domain += ['|',
                        ('subject', 'ilike', search),
                        ('name', 'ilike', search)]
        if status:
            domain.append(('state', '=', status))

        Msg = request.env['education.message'].sudo()
        total = Msg.search_count(domain)
        messages = Msg.search(domain, order='create_date desc',
                              limit=limit, offset=offset)

        result = []
        for m in messages:
            result.append({
                'id': m.id,
                'name': m.name or '',
                'subject': m.subject or '',
                'recipient_type': m.recipient_type or '',
                'state': m.state,
                'recipient_count': m.recipient_count if hasattr(m, 'recipient_count') else 0,
                'sent_count': m.sent_count if hasattr(m, 'sent_count') else 0,
                'scheduled_date': str(m.scheduled_date) if m.scheduled_date else '',
                'sent_date': str(m.sent_date) if m.sent_date else '',
                'created_by': m.created_by.name if m.created_by else '',
            })

        return json_response({
            'messages': result,
            'total': total,
            'page': page,
            'pages': (total + limit - 1) // limit if limit else 1,
        })

    # ─── Options (dropdowns) ────────────────────────────────

    @http.route('/api/admin/options', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def admin_options(self, **kwargs):
        """Return dropdown options for forms."""
        env = request.env

        departments = env['education.department'].sudo().search([])
        classes = env['education.class'].sudo().search([])
        branches = env['education.branch'].sudo().search([])
        guardians = env['res.partner'].sudo().search(
            [('is_guardian', '=', True)], order='name', limit=500)

        return json_response({
            'departments': [{'id': d.id, 'name': d.name} for d in departments],
            'classes': [{'id': c.id, 'name': c.name,
                         'department_id': c.department_id.id if c.department_id else None}
                        for c in classes],
            'branches': [{'id': b.id, 'name': b.name} for b in branches],
            'guardians': [{'id': g.id, 'name': g.name} for g in guardians],
        })

    # ─── Create Student ─────────────────────────────────────

    @http.route('/api/admin/students/create', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_student(self, **kwargs):
        """Create a new student."""
        data = get_request_data()
        if not data.get('name'):
            return error_response('اسم الطالب مطلوب', 400, 'VALIDATION_ERROR')

        vals = {
            'name': data['name'],
            'is_student': True,
            'student_state': 'draft',
        }
        if data.get('arabic_name'):
            vals['arabic_name'] = data['arabic_name']
        if data.get('gender'):
            vals['gender'] = data['gender']
        if data.get('birthdate'):
            vals['birthdate'] = data['birthdate']
        if data.get('department_id'):
            vals['department_id'] = int(data['department_id'])
        if data.get('class_id'):
            vals['class_id'] = int(data['class_id'])
        if data.get('father_id'):
            vals['father_id'] = int(data['father_id'])
        if data.get('mother_id'):
            vals['mother_id'] = int(data['mother_id'])
        if data.get('period'):
            vals['period'] = data['period']
        if data.get('branch_id'):
            vals['branch_id'] = int(data['branch_id'])
        if data.get('phone'):
            vals['phone'] = data['phone']
        if data.get('religion'):
            vals['religion'] = data['religion']
        if data.get('blood_type'):
            vals['blood_type'] = data['blood_type']
        if data.get('allergies'):
            vals['allergies'] = data['allergies']
        if data.get('medical_notes'):
            vals['medical_notes'] = data['medical_notes']

        try:
            student = request.env['res.partner'].sudo().create(vals)
            return json_response({
                'id': student.id,
                'code': student.code or '',
                'name': student.name,
                'message': 'تم إضافة الطالب بنجاح',
            })
        except Exception as e:
            _logger.exception('Failed to create student')
            return error_response(str(e), 500, 'CREATE_FAILED')

    # ─── Create Teacher ─────────────────────────────────────

    @http.route('/api/admin/teachers/create', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_teacher(self, **kwargs):
        """Create a new teacher."""
        data = get_request_data()
        if not data.get('name'):
            return error_response('اسم المعلم مطلوب', 400, 'VALIDATION_ERROR')

        vals = {
            'name': data['name'],
            'is_teacher': True,
            'state': 'draft',
        }
        if data.get('phone'):
            vals['phone'] = data['phone']
        if data.get('mobile'):
            vals['mobile'] = data['mobile']
        if data.get('email'):
            vals['email'] = data['email']
        if data.get('gender'):
            vals['gender'] = data['gender']
        if data.get('birthdate'):
            vals['birthdate'] = data['birthdate']
        if data.get('job_title'):
            vals['job_title'] = data['job_title']
        if data.get('department_id'):
            vals['department_id'] = int(data['department_id'])
        if data.get('branch_id'):
            vals['branch_id'] = int(data['branch_id'])
        if data.get('shift_type'):
            vals['shift_type'] = data['shift_type']
        if data.get('hire_date'):
            vals['hire_date'] = data['hire_date']
        if data.get('salary'):
            vals['salary'] = float(data['salary'])
        if data.get('id_number'):
            vals['id_number'] = data['id_number']
        if data.get('qualification'):
            vals['qualification'] = data['qualification']

        try:
            teacher = request.env['education.employee'].sudo().create(vals)
            return json_response({
                'id': teacher.id,
                'code': teacher.code or '',
                'name': teacher.name,
                'message': 'تم إضافة المعلم بنجاح',
            })
        except Exception as e:
            _logger.exception('Failed to create teacher')
            return error_response(str(e), 500, 'CREATE_FAILED')

    # ─── Create Parent ───────────────────────────────────────

    @http.route('/api/admin/parents/create', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_parent(self, **kwargs):
        """Create a new parent/guardian."""
        data = get_request_data()
        if not data.get('name'):
            return error_response('اسم ولي الأمر مطلوب', 400, 'VALIDATION_ERROR')

        vals = {
            'name': data['name'],
            'is_guardian': True,
        }
        if data.get('phone'):
            vals['phone'] = data['phone']
        if data.get('email'):
            vals['email'] = data['email']
        if data.get('guardian_relation'):
            vals['guardian_relation'] = data['guardian_relation']
        if data.get('id_number'):
            vals['id_number'] = data['id_number']
        if data.get('workplace'):
            vals['workplace'] = data['workplace']
        if data.get('parent_social_status'):
            vals['parent_social_status'] = data['parent_social_status']
        if data.get('education_level'):
            vals['education_level'] = data['education_level']

        try:
            parent = request.env['res.partner'].sudo().create(vals)
            return json_response({
                'id': parent.id,
                'name': parent.name,
                'message': 'تم إضافة ولي الأمر بنجاح',
            })
        except Exception as e:
            _logger.exception('Failed to create parent')
            return error_response(str(e), 500, 'CREATE_FAILED')

    # ─── Student Detail ─────────────────────────────────────

    @http.route('/api/admin/students/<int:student_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def student_detail(self, student_id, **kwargs):
        """Get student detail."""
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        portal_user = self._get_portal_user_info(s)

        children_of_father = []
        if s.father_id:
            for sib in s.father_id.father_student_ids:
                if sib.id != s.id:
                    children_of_father.append({'id': sib.id, 'name': sib.name})

        return json_response({
            'id': s.id,
            'name': s.name,
            'arabic_name': s.arabic_name or '',
            'code': s.code or '',
            'gender': s.gender or '',
            'birthdate': str(s.birthdate) if s.birthdate else '',
            'age': s.age or '',
            'department': s.department_id.name if s.department_id else '',
            'department_id': s.department_id.id if s.department_id else None,
            'class_name': s.class_id.name if s.class_id else '',
            'class_id': s.class_id.id if s.class_id else None,
            'branch': s.branch_id.name if s.branch_id else '',
            'period': s.period or '',
            'state': s.student_state or 'draft',
            'active': s.active,
            'enrollment_date': str(s.enrollment_date) if s.enrollment_date else '',
            'phone': s.phone or '',
            'email': s.email or '',
            'religion': getattr(s, 'religion', '') or '',
            'blood_type': getattr(s, 'blood_type', '') or '',
            'allergies': s.allergies or '',
            'medical_notes': s.medical_notes or '',
            'father': {'id': s.father_id.id, 'name': s.father_id.name} if s.father_id else None,
            'mother': {'id': s.mother_id.id, 'name': s.mother_id.name} if s.mother_id else None,
            'siblings': children_of_father,
            'balance_due': s.balance_due or 0,
            'attendance_rate': s.attendance_rate or 0,
            'subscription_count': s.subscription_count or 0,
            'portal_user': portal_user,
        })

    # ─── Teacher Detail ─────────────────────────────────────

    @http.route('/api/admin/teachers/<int:teacher_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def teacher_detail(self, teacher_id, **kwargs):
        """Get teacher detail."""
        t = request.env['education.employee'].sudo().browse(teacher_id)
        if not t.exists():
            return error_response('Teacher not found', 404, 'NOT_FOUND')

        classes = [{'id': c.id, 'name': c.name} for c in t.assigned_class_ids] if t.assigned_class_ids else []

        # Portal user — teacher may have a linked partner
        portal_user = None
        partner = getattr(t, 'partner_id', None)
        if partner:
            portal_user = self._get_portal_user_info(partner)

        return json_response({
            'id': t.id,
            'name': t.name or '',
            'code': t.code or '',
            'gender': t.gender or '',
            'birthdate': str(t.birthdate) if t.birthdate else '',
            'age': t.age or 0,
            'phone': t.phone or '',
            'mobile': t.mobile or '',
            'email': t.email or '',
            'id_number': t.id_number or '',
            'job_title': t.job_title or '',
            'qualification': getattr(t, 'qualification', '') or '',
            'department': t.department_id.name if t.department_id else '',
            'department_id': t.department_id.id if t.department_id else None,
            'branch': t.branch_id.name if t.branch_id else '',
            'branch_id': t.branch_id.id if t.branch_id else None,
            'shift_type': t.shift_type or '',
            'hire_date': str(t.hire_date) if t.hire_date else '',
            'end_date': str(t.end_date) if t.end_date else '',
            'salary': t.salary or 0,
            'state': t.state or 'draft',
            'active': t.active,
            'classes': classes,
            'class_count': t.class_count if hasattr(t, 'class_count') else 0,
            'attendance_count': t.attendance_count if hasattr(t, 'attendance_count') else 0,
            'portal_user': portal_user,
        })

    # ─── Parent Detail ───────────────────────────────────────

    @http.route('/api/admin/parents/<int:parent_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def parent_detail(self, parent_id, **kwargs):
        """Get parent/guardian detail."""
        p = request.env['res.partner'].sudo().browse(parent_id)
        if not p.exists() or not p.is_guardian:
            return error_response('Parent not found', 404, 'NOT_FOUND')

        portal_user = self._get_portal_user_info(p)

        children = []
        all_kids = p._get_all_children() if hasattr(p, '_get_all_children') else (p.father_student_ids | p.mother_student_ids)
        for c in all_kids:
            children.append({
                'id': c.id,
                'name': c.name,
                'code': c.code or '',
                'department': c.department_id.name if c.department_id else '',
                'class_name': c.class_id.name if c.class_id else '',
                'state': c.student_state or '',
            })

        return json_response({
            'id': p.id,
            'name': p.name,
            'phone': p.phone or '',
            'email': p.email or '',
            'guardian_relation': p.guardian_relation or '',
            'id_number': getattr(p, 'id_number', '') or '',
            'workplace': getattr(p, 'workplace', '') or '',
            'parent_social_status': getattr(p, 'parent_social_status', '') or '',
            'education_level': getattr(p, 'education_level', '') or '',
            'active': p.active,
            'children': children,
            'children_count': p.children_count or 0,
            'children_balance_due': p.children_balance_due or 0,
            'children_attendance_pct': p.children_attendance_pct or 0,
            'total_paid': p.total_paid or 0,
            'total_remaining': p.total_remaining or 0,
            'portal_user': portal_user,
        })

    # ─── Student Action ──────────────────────────────────────

    @http.route('/api/admin/students/<int:student_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def student_action(self, student_id, **kwargs):
        """Perform action on student: enroll, suspend, archive, reactivate."""
        data = get_request_data()
        action = data.get('action')
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        try:
            if action == 'pending':
                s.action_pending()
            elif action == 'enroll':
                s.action_enroll()
            elif action == 'suspend':
                s.action_suspend()
            elif action == 'archive':
                s.action_archive_student()
            elif action == 'reactivate':
                s.action_reactivate()
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'state': s.student_state, 'active': s.active})
        except Exception as e:
            _logger.exception('Student action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Teacher Action ──────────────────────────────────────

    @http.route('/api/admin/teachers/<int:teacher_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def teacher_action(self, teacher_id, **kwargs):
        """Perform action on teacher: activate, on_leave, terminate, reactivate."""
        data = get_request_data()
        action = data.get('action')
        t = request.env['education.employee'].sudo().browse(teacher_id)
        if not t.exists():
            return error_response('Teacher not found', 404, 'NOT_FOUND')

        try:
            if action == 'activate':
                t.action_activate()
            elif action == 'on_leave':
                t.action_on_leave()
            elif action == 'terminate':
                t.action_terminate()
            elif action == 'reactivate':
                t.action_reactivate()
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'state': t.state, 'active': t.active})
        except Exception as e:
            _logger.exception('Teacher action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Parent Action ───────────────────────────────────────

    @http.route('/api/admin/parents/<int:parent_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def parent_action(self, parent_id, **kwargs):
        """Archive or reactivate parent."""
        data = get_request_data()
        action = data.get('action')
        p = request.env['res.partner'].sudo().browse(parent_id)
        if not p.exists() or not p.is_guardian:
            return error_response('Parent not found', 404, 'NOT_FOUND')

        try:
            if action == 'archive':
                p.active = False
            elif action == 'reactivate':
                p.active = True
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'active': p.active})
        except Exception as e:
            _logger.exception('Parent action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Portal User Management ──────────────────────────────

    @http.route('/api/admin/portal-user/create', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_portal_user(self, **kwargs):
        """Create portal account for a partner."""
        data = get_request_data()
        partner_id = data.get('partner_id')
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        user_type = data.get('user_type', 'parent')

        if not partner_id or not username or not password:
            return error_response('partner_id, username, password مطلوبة', 400, 'VALIDATION_ERROR')

        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner.exists():
            return error_response('Partner not found', 404, 'NOT_FOUND')

        PortalUser = request.env['dar.portal.user'].sudo()
        existing = PortalUser.search([('partner_id', '=', partner.id)], limit=1)
        if existing:
            return error_response('هذا الشخص لديه حساب بالفعل', 400, 'ALREADY_EXISTS')

        try:
            pu = PortalUser.create({
                'partner_id': partner.id,
                'username': username,
                'user_type': user_type,
                'is_active': True,
            })
            pu.set_password(password)
            return json_response({
                'id': pu.id,
                'username': pu.username,
                'message': 'تم إنشاء الحساب بنجاح',
            })
        except Exception as e:
            _logger.exception('Failed to create portal user')
            return error_response(str(e), 500, 'CREATE_FAILED')

    @http.route('/api/admin/portal-user/<int:pu_id>/toggle', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def toggle_portal_user(self, pu_id, **kwargs):
        """Enable/disable portal user account."""
        pu = request.env['dar.portal.user'].sudo().browse(pu_id)
        if not pu.exists():
            return error_response('Portal user not found', 404, 'NOT_FOUND')

        pu.action_toggle_active()
        return json_response({
            'is_active': pu.is_active,
            'message': 'تم تفعيل الحساب' if pu.is_active else 'تم تعطيل الحساب',
        })

    @http.route('/api/admin/portal-user/<int:pu_id>/reset-password', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def reset_portal_password(self, pu_id, **kwargs):
        """Reset portal user password."""
        data = get_request_data()
        new_password = data.get('password', '').strip()
        if not new_password or len(new_password) < 6:
            return error_response('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 400, 'VALIDATION_ERROR')

        pu = request.env['dar.portal.user'].sudo().browse(pu_id)
        if not pu.exists():
            return error_response('Portal user not found', 404, 'NOT_FOUND')

        pu.set_password(new_password)
        return json_response({'message': 'تم تغيير كلمة المرور بنجاح'})

    # ─── Subscription Detail ─────────────────────────────────

    @http.route('/api/admin/subscriptions/<int:sub_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def subscription_detail(self, sub_id, **kwargs):
        """Get subscription detail."""
        sub = request.env['education.student.subscription'].sudo().browse(sub_id)
        if not sub.exists():
            return error_response('Subscription not found', 404, 'NOT_FOUND')

        installments = []
        for inst in sub.installment_ids:
            installments.append({
                'id': inst.id,
                'sequence': inst.sequence or 0,
                'due_date': str(inst.due_date) if inst.due_date else '',
                'amount': inst.amount or 0,
                'paid_amount': inst.paid_amount or 0,
                'remaining_amount': inst.remaining_amount or 0,
                'is_paid': inst.is_paid,
            })

        return json_response({
            'id': sub.id,
            'student': sub.student_id.name if sub.student_id else '',
            'student_id': sub.student_id.id if sub.student_id else None,
            'student_code': sub.student_id.code if sub.student_id else '',
            'subscription_type': sub.subscription_type_id.name if sub.subscription_type_id else '',
            'payment_plan': sub.payment_plan_id.name if sub.payment_plan_id else '',
            'start_date': str(sub.start_date) if sub.start_date else '',
            'end_date': str(sub.end_date) if sub.end_date else '',
            'academic_year': sub.academic_year_id.name if sub.academic_year_id else '',
            'total_amount': sub.total_amount or 0,
            'discount': sub.discount or 0,
            'discount_type': sub.discount_type or '',
            'discount_amount': sub.discount_amount or 0,
            'net_amount': sub.net_amount or 0,
            'paid_amount': sub.paid_amount or 0,
            'remaining_amount': sub.remaining_amount or 0,
            'status': sub.status or 'draft',
            'notes': sub.notes or '',
            'installments': installments,
            'installment_count': sub.installment_count or 0,
            'invoice_count': sub.invoice_count or 0,
        })

    # ─── Subscription Action ─────────────────────────────────

    @http.route('/api/admin/subscriptions/<int:sub_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def subscription_action(self, sub_id, **kwargs):
        """Activate, expire, or cancel a subscription."""
        data = get_request_data()
        action = data.get('action')
        sub = request.env['education.student.subscription'].sudo().browse(sub_id)
        if not sub.exists():
            return error_response('Subscription not found', 404, 'NOT_FOUND')

        try:
            if action == 'activate':
                sub.status = 'active'
            elif action == 'expire':
                sub.status = 'expired'
            elif action == 'cancel':
                sub.status = 'cancelled'
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'status': sub.status})
        except Exception as e:
            _logger.exception('Subscription action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Invoice Detail ──────────────────────────────────────

    @http.route('/api/admin/invoices/<int:inv_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def invoice_detail(self, inv_id, **kwargs):
        """Get invoice detail."""
        inv = request.env['account.move'].sudo().browse(inv_id)
        if not inv.exists():
            return error_response('Invoice not found', 404, 'NOT_FOUND')

        lines = []
        for ln in inv.invoice_line_ids:
            lines.append({
                'id': ln.id,
                'name': ln.name or '',
                'quantity': ln.quantity or 0,
                'price_unit': ln.price_unit or 0,
                'price_subtotal': ln.price_subtotal or 0,
            })

        payments = []
        if hasattr(inv, '_get_reconciled_payments'):
            for pay in inv._get_reconciled_payments():
                payments.append({
                    'id': pay.id,
                    'date': str(pay.date) if pay.date else '',
                    'amount': pay.amount or 0,
                    'journal': pay.journal_id.name if pay.journal_id else '',
                })

        return json_response({
            'id': inv.id,
            'name': inv.name or '',
            'partner': inv.partner_id.name if inv.partner_id else '',
            'partner_id': inv.partner_id.id if inv.partner_id else None,
            'date': str(inv.invoice_date) if inv.invoice_date else '',
            'due_date': str(inv.invoice_date_due) if inv.invoice_date_due else '',
            'amount_untaxed': inv.amount_untaxed or 0,
            'amount_tax': inv.amount_tax or 0,
            'amount_total': inv.amount_total or 0,
            'amount_residual': inv.amount_residual or 0,
            'amount_paid': (inv.amount_total or 0) - (inv.amount_residual or 0),
            'state': inv.state or '',
            'payment_state': inv.payment_state or '',
            'move_type': inv.move_type or '',
            'ref': inv.ref or '',
            'narration': inv.narration or '',
            'lines': lines,
            'payments': payments,
        })

    # ─── Attendance Detail ────────────────────────────────────

    @http.route('/api/admin/attendance/<int:att_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def attendance_detail(self, att_id, **kwargs):
        """Get attendance record detail."""
        att = request.env['education.attendance'].sudo().browse(att_id)
        if not att.exists():
            return error_response('Attendance not found', 404, 'NOT_FOUND')

        lines = []
        for ln in att.line_ids:
            lines.append({
                'id': ln.id,
                'student': ln.student_id.name if ln.student_id else '',
                'student_id': ln.student_id.id if ln.student_id else None,
                'status': ln.status or 'present',
                'notes': ln.notes or '',
                'check_in_time': str(ln.check_in_time) if ln.check_in_time else '',
                'check_out_time': str(ln.check_out_time) if ln.check_out_time else '',
                'late_minutes': ln.late_minutes or 0,
            })

        return json_response({
            'id': att.id,
            'date': str(att.date) if att.date else '',
            'department': att.department_id.name if att.department_id else '',
            'department_id': att.department_id.id if att.department_id else None,
            'class_name': att.class_id.name if att.class_id else '',
            'class_id': att.class_id.id if att.class_id else None,
            'recorded_by': att.recorded_by.name if att.recorded_by else '',
            'state': att.state or 'draft',
            'notes': att.notes or '',
            'present_count': att.present_count or 0,
            'absent_count': att.absent_count or 0,
            'late_count': att.late_count or 0,
            'total_count': att.total_count or 0,
            'lines': lines,
        })

    # ─── Attendance Action ────────────────────────────────────

    @http.route('/api/admin/attendance/<int:att_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def attendance_action(self, att_id, **kwargs):
        """Confirm or lock attendance."""
        data = get_request_data()
        action = data.get('action')
        att = request.env['education.attendance'].sudo().browse(att_id)
        if not att.exists():
            return error_response('Attendance not found', 404, 'NOT_FOUND')

        try:
            if action == 'confirm':
                att.state = 'confirmed'
            elif action == 'lock':
                att.state = 'locked'
            elif action == 'draft':
                att.state = 'draft'
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'state': att.state})
        except Exception as e:
            _logger.exception('Attendance action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Content Detail ──────────────────────────────────────

    @http.route('/api/admin/content/<int:content_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def content_detail(self, content_id, **kwargs):
        """Get content item detail."""
        c = request.env['education.content.item'].sudo().browse(content_id)
        if not c.exists():
            return error_response('Content not found', 404, 'NOT_FOUND')

        return json_response({
            'id': c.id,
            'name': c.name or '',
            'category': c.category_id.name if c.category_id else '',
            'category_id': c.category_id.id if c.category_id else None,
            'content_type': c.content_type or '',
            'description': c.description or '',
            'file_url': c.file_url or '',
            'file_name': c.file_name or '',
            'has_file': bool(c.file),
            'target_age_min': c.target_age_min or 0,
            'target_age_max': c.target_age_max or 0,
            'is_drm_protected': c.is_drm_protected or False,
            'active': c.active,
            'access_count': c.access_count or 0,
            'grade_levels': [{'id': g.id, 'name': g.name} for g in c.grade_level_ids] if c.grade_level_ids else [],
        })

    # ─── Content Action ──────────────────────────────────────

    @http.route('/api/admin/content/<int:content_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def content_action(self, content_id, **kwargs):
        """Activate or deactivate content."""
        data = get_request_data()
        action = data.get('action')
        c = request.env['education.content.item'].sudo().browse(content_id)
        if not c.exists():
            return error_response('Content not found', 404, 'NOT_FOUND')

        try:
            if action == 'activate':
                c.active = True
            elif action == 'deactivate':
                c.active = False
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'active': c.active})
        except Exception as e:
            _logger.exception('Content action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Kids Area Booking Detail ─────────────────────────────

    @http.route('/api/admin/kidsarea/booking/<int:booking_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def kidsarea_booking_detail(self, booking_id, **kwargs):
        """Get kids area booking detail."""
        b = request.env['education.kids.area.booking'].sudo().browse(booking_id)
        if not b.exists():
            return error_response('Booking not found', 404, 'NOT_FOUND')

        slot_info = {}
        if b.slot_id:
            slot_info = {
                'id': b.slot_id.id,
                'date': str(b.slot_id.date) if b.slot_id.date else '',
                'time_from': b.slot_id.time_from or 0,
                'time_to': b.slot_id.time_to or 0,
                'service': b.slot_id.service_id.name if b.slot_id.service_id else '',
                'service_id': b.slot_id.service_id.id if b.slot_id.service_id else None,
                'capacity': b.slot_id.capacity or 0,
                'booked_count': b.slot_id.booked_count or 0,
                'supervisor': b.slot_id.supervisor_id.name if b.slot_id.supervisor_id else '',
            }

        return json_response({
            'id': b.id,
            'student': b.student_id.name if b.student_id else '',
            'student_id': b.student_id.id if b.student_id else None,
            'parent': b.parent_id.name if b.parent_id else '',
            'parent_id': b.parent_id.id if b.parent_id else None,
            'booking_date': str(b.booking_date) if b.booking_date else '',
            'state': b.state or 'draft',
            'amount': b.amount or 0,
            'payment_status': b.payment_status or 'pending',
            'qr_code': b.qr_code or '',
            'notes': b.notes or '',
            'slot': slot_info,
        })

    # ─── Kids Area Booking Action ─────────────────────────────

    @http.route('/api/admin/kidsarea/booking/<int:booking_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def kidsarea_booking_action(self, booking_id, **kwargs):
        """Update booking state."""
        data = get_request_data()
        action = data.get('action')
        b = request.env['education.kids.area.booking'].sudo().browse(booking_id)
        if not b.exists():
            return error_response('Booking not found', 404, 'NOT_FOUND')

        valid_states = ['draft', 'confirmed', 'checked_in', 'checked_out', 'cancelled', 'no_show']
        try:
            if action == 'confirm':
                b.state = 'confirmed'
            elif action == 'check_in':
                b.state = 'checked_in'
            elif action == 'check_out':
                b.state = 'checked_out'
            elif action == 'cancel':
                b.state = 'cancelled'
            elif action == 'no_show':
                b.state = 'no_show'
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'state': b.state})
        except Exception as e:
            _logger.exception('Booking action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Message Detail ──────────────────────────────────────

    @http.route('/api/admin/messages/<int:msg_id>', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def message_detail(self, msg_id, **kwargs):
        """Get message detail."""
        m = request.env['education.message'].sudo().browse(msg_id)
        if not m.exists():
            return error_response('Message not found', 404, 'NOT_FOUND')

        recipients = []
        if m.recipient_type == 'individual' and m.student_ids:
            for s in m.student_ids[:50]:
                recipients.append({'id': s.id, 'name': s.name})

        logs = []
        for lg in m.log_ids[:50]:
            logs.append({
                'id': lg.id,
                'recipient': lg.recipient_id.name if hasattr(lg, 'recipient_id') and lg.recipient_id else '',
                'status': lg.status if hasattr(lg, 'status') else '',
                'sent_date': str(lg.sent_date) if hasattr(lg, 'sent_date') and lg.sent_date else '',
            })

        return json_response({
            'id': m.id,
            'name': m.name or '',
            'subject': m.subject or '',
            'body': m.body or '',
            'recipient_type': m.recipient_type or '',
            'department': m.department_id.name if m.department_id else '',
            'department_id': m.department_id.id if m.department_id else None,
            'class_name': m.class_id.name if m.class_id else '',
            'class_id': m.class_id.id if m.class_id else None,
            'state': m.state or 'draft',
            'scheduled_date': str(m.scheduled_date) if m.scheduled_date else '',
            'sent_date': str(m.sent_date) if m.sent_date else '',
            'created_by': m.created_by.name if m.created_by else '',
            'recipient_count': m.recipient_count or 0,
            'sent_count': m.sent_count or 0,
            'failed_count': m.failed_count or 0,
            'recipients': recipients,
            'logs': logs,
        })

    # ─── Message Action ──────────────────────────────────────

    @http.route('/api/admin/messages/<int:msg_id>/action', type='http', auth='none',
                methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def message_action(self, msg_id, **kwargs):
        """Send, schedule, or cancel a message."""
        data = get_request_data()
        action = data.get('action')
        m = request.env['education.message'].sudo().browse(msg_id)
        if not m.exists():
            return error_response('Message not found', 404, 'NOT_FOUND')

        try:
            if action == 'send':
                if hasattr(m, 'action_send'):
                    m.action_send()
                else:
                    m.state = 'sent'
                    m.sent_date = fields.Datetime.now()
            elif action == 'cancel':
                m.state = 'cancelled'
            elif action == 'draft':
                m.state = 'draft'
            else:
                return error_response('Invalid action', 400, 'INVALID_ACTION')
            return json_response({'message': 'تم تنفيذ الإجراء بنجاح', 'state': m.state})
        except Exception as e:
            _logger.exception('Message action failed')
            return error_response(str(e), 500, 'ACTION_FAILED')

    # ─── Subscription Options ─────────────────────────────────

    @http.route('/api/admin/subscription-options', type='http', auth='none',
                methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def subscription_options(self, **kwargs):
        """Return subscription types, payment plans, and content items for dropdowns."""
        env = request.env
        sub_types = env['education.subscription.type'].sudo().search([('active', '=', True)])
        plans = env['education.payment.plan'].sudo().search([])
        items = env['education.content.item'].sudo().search([('active', '=', True)])

        return json_response({
            'subscription_types': [{
                'id': st.id,
                'name': st.display_name or st.name,
                'amount': st.amount,
                'department': st.department_id.name if st.department_id else '',
                'payment_plan_id': st.payment_plan_id.id if st.payment_plan_id else None,
            } for st in sub_types],
            'payment_plans': [{
                'id': pp.id,
                'name': pp.name,
                'installment_count': pp.installment_count,
                'interval_months': pp.interval_months,
            } for pp in plans],
            'content_items': [{
                'id': ci.id,
                'name': ci.name,
                'content_type': ci.content_type or '',
                'category': ci.category_id.name if ci.category_id else '',
            } for ci in items],
        })

    # ─── Student Subscriptions ────────────────────────────────

    @http.route('/api/admin/students/<int:student_id>/subscriptions', type='http',
                auth='none', methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def student_subscriptions(self, student_id, **kwargs):
        """Get all subscriptions for a student with installments."""
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        subs = request.env['education.student.subscription'].sudo().search(
            [('student_id', '=', student_id)], order='start_date desc')

        result = []
        for sub in subs:
            installments = []
            for inst in sub.installment_ids.sorted('sequence'):
                installments.append({
                    'id': inst.id,
                    'sequence': inst.sequence,
                    'due_date': str(inst.due_date) if inst.due_date else '',
                    'amount': inst.amount,
                    'paid_amount': inst.paid_amount,
                    'remaining_amount': inst.remaining_amount,
                    'is_paid': inst.is_paid,
                })
            result.append({
                'id': sub.id,
                'type': sub.subscription_type_id.name if sub.subscription_type_id else '',
                'type_id': sub.subscription_type_id.id if sub.subscription_type_id else None,
                'plan': sub.payment_plan_id.name if sub.payment_plan_id else '',
                'start_date': str(sub.start_date) if sub.start_date else '',
                'end_date': str(sub.end_date) if sub.end_date else '',
                'total_amount': sub.total_amount,
                'discount': sub.discount,
                'net_amount': sub.net_amount,
                'paid_amount': sub.paid_amount,
                'remaining_amount': sub.remaining_amount,
                'status': sub.status,
                'notes': sub.notes or '',
                'installments': installments,
            })
        return json_response({'subscriptions': result})

    # ─── Student Content Access ───────────────────────────────

    @http.route('/api/admin/students/<int:student_id>/content-access', type='http',
                auth='none', methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def student_content_access(self, student_id, **kwargs):
        """Get content access list for a student."""
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        accesses = request.env['education.content.access'].sudo().search(
            [('student_id', '=', student_id)], order='granted_date desc')

        result = []
        for a in accesses:
            result.append({
                'id': a.id,
                'content_name': a.content_item_id.name if a.content_item_id else '',
                'content_type': a.content_item_id.content_type if a.content_item_id else '',
                'category': a.content_item_id.category_id.name if a.content_item_id and a.content_item_id.category_id else '',
                'granted_date': str(a.granted_date) if a.granted_date else '',
                'expiry_date': str(a.expiry_date) if a.expiry_date else '',
                'is_active': a.is_active,
            })
        return json_response({'content_access': result})

    # ─── Grant Content to Student ─────────────────────────────

    @http.route('/api/admin/students/<int:student_id>/grant-content', type='http',
                auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def grant_content_to_student(self, student_id, **kwargs):
        """Grant content items to a student."""
        data = get_request_data()
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        content_item_ids = data.get('content_item_ids', [])
        if not content_item_ids:
            return error_response('لم يتم اختيار محتوى', 400, 'VALIDATION_ERROR')

        expiry_date = data.get('expiry_date') or False
        Access = request.env['education.content.access'].sudo()
        granted = 0
        skipped = 0

        for item_id in content_item_ids:
            existing = Access.search([
                ('student_id', '=', student_id),
                ('content_item_id', '=', int(item_id)),
                ('is_active', '=', True),
            ], limit=1)
            if existing:
                skipped += 1
                continue
            Access.create({
                'student_id': student_id,
                'content_item_id': int(item_id),
                'expiry_date': expiry_date,
            })
            granted += 1

        return json_response({
            'message': f'تم منح {granted} محتوى' + (f' (تم تخطي {skipped} موجود بالفعل)' if skipped else ''),
            'granted': granted,
            'skipped': skipped,
        })

    # ─── Create Subscription for Student ──────────────────────

    @http.route('/api/admin/students/<int:student_id>/create-subscription', type='http',
                auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_student_subscription(self, student_id, **kwargs):
        """Create a new subscription for a student and generate installments."""
        data = get_request_data()
        s = request.env['res.partner'].sudo().browse(student_id)
        if not s.exists() or not s.is_student:
            return error_response('Student not found', 404, 'NOT_FOUND')

        sub_type_id = data.get('subscription_type_id')
        plan_id = data.get('payment_plan_id')
        if not sub_type_id or not plan_id:
            return error_response('نوع الاشتراك وخطة الدفع مطلوبان', 400, 'VALIDATION_ERROR')

        total = data.get('total_amount')
        if not total:
            sub_type = request.env['education.subscription.type'].sudo().browse(int(sub_type_id))
            total = sub_type.amount if sub_type.exists() else 0

        vals = {
            'student_id': student_id,
            'subscription_type_id': int(sub_type_id),
            'payment_plan_id': int(plan_id),
            'start_date': data.get('start_date') or fields.Date.context_today(request.env.user),
            'total_amount': float(total),
            'discount': float(data.get('discount', 0)),
            'notes': data.get('notes', ''),
        }

        try:
            sub = request.env['education.student.subscription'].sudo().create(vals)
            sub.action_generate_installments()
            return json_response({
                'message': 'تم إنشاء الاشتراك بنجاح',
                'subscription_id': sub.id,
                'status': sub.status,
            })
        except Exception as e:
            _logger.exception('Failed to create subscription')
            return error_response(str(e), 500, 'CREATE_FAILED')

    # ─── Parent Children Data ─────────────────────────────────

    @http.route('/api/admin/parents/<int:parent_id>/children-data', type='http',
                auth='none', methods=['GET'], csrf=False, cors='*')
    @admin_jwt_required
    def parent_children_data(self, parent_id, **kwargs):
        """Get all children subscriptions + content access for a parent."""
        p = request.env['res.partner'].sudo().browse(parent_id)
        if not p.exists() or not p.is_guardian:
            return error_response('Parent not found', 404, 'NOT_FOUND')

        all_kids = p._get_all_children() if hasattr(p, '_get_all_children') else (p.father_student_ids | p.mother_student_ids)

        children_data = []
        for child in all_kids:
            # Subscriptions
            subs = request.env['education.student.subscription'].sudo().search(
                [('student_id', '=', child.id)], order='start_date desc')
            child_subs = []
            for sub in subs:
                installments = [{
                    'id': inst.id,
                    'sequence': inst.sequence,
                    'due_date': str(inst.due_date) if inst.due_date else '',
                    'amount': inst.amount,
                    'paid_amount': inst.paid_amount,
                    'is_paid': inst.is_paid,
                } for inst in sub.installment_ids.sorted('sequence')]
                child_subs.append({
                    'id': sub.id,
                    'type': sub.subscription_type_id.name if sub.subscription_type_id else '',
                    'start_date': str(sub.start_date) if sub.start_date else '',
                    'total_amount': sub.total_amount,
                    'net_amount': sub.net_amount,
                    'paid_amount': sub.paid_amount,
                    'remaining_amount': sub.remaining_amount,
                    'status': sub.status,
                    'installments': installments,
                })

            # Content access
            accesses = request.env['education.content.access'].sudo().search(
                [('student_id', '=', child.id)], order='granted_date desc')
            child_content = [{
                'id': a.id,
                'content_name': a.content_item_id.name if a.content_item_id else '',
                'content_type': a.content_item_id.content_type if a.content_item_id else '',
                'granted_date': str(a.granted_date) if a.granted_date else '',
                'expiry_date': str(a.expiry_date) if a.expiry_date else '',
                'is_active': a.is_active,
            } for a in accesses]

            children_data.append({
                'id': child.id,
                'name': child.name,
                'code': child.code or '',
                'subscriptions': child_subs,
                'content_access': child_content,
            })

        return json_response({'children': children_data})

    # ─── Grant Content to All Children of Parent ──────────────

    @http.route('/api/admin/parents/<int:parent_id>/grant-content', type='http',
                auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def grant_content_to_parent_children(self, parent_id, **kwargs):
        """Grant content to ALL children of a parent (cascade)."""
        data = get_request_data()
        p = request.env['res.partner'].sudo().browse(parent_id)
        if not p.exists() or not p.is_guardian:
            return error_response('Parent not found', 404, 'NOT_FOUND')

        content_item_ids = data.get('content_item_ids', [])
        if not content_item_ids:
            return error_response('لم يتم اختيار محتوى', 400, 'VALIDATION_ERROR')

        expiry_date = data.get('expiry_date') or False
        all_kids = p._get_all_children() if hasattr(p, '_get_all_children') else (p.father_student_ids | p.mother_student_ids)
        Access = request.env['education.content.access'].sudo()

        total_granted = 0
        total_skipped = 0
        for child in all_kids:
            for item_id in content_item_ids:
                existing = Access.search([
                    ('student_id', '=', child.id),
                    ('content_item_id', '=', int(item_id)),
                    ('is_active', '=', True),
                ], limit=1)
                if existing:
                    total_skipped += 1
                    continue
                Access.create({
                    'student_id': child.id,
                    'content_item_id': int(item_id),
                    'expiry_date': expiry_date,
                })
                total_granted += 1

        return json_response({
            'message': f'تم منح {total_granted} محتوى لـ {len(all_kids)} طالب'
                       + (f' (تم تخطي {total_skipped} موجود)' if total_skipped else ''),
            'granted': total_granted,
            'skipped': total_skipped,
            'children_count': len(all_kids),
        })

    # ─── Revoke Content Access ────────────────────────────────

    @http.route('/api/admin/content-access/<int:access_id>/revoke', type='http',
                auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def revoke_content_access(self, access_id, **kwargs):
        """Revoke a content access grant."""
        access = request.env['education.content.access'].sudo().browse(access_id)
        if not access.exists():
            return error_response('Access grant not found', 404, 'NOT_FOUND')

        access.action_revoke()
        return json_response({'message': 'تم إلغاء الوصول بنجاح'})

    # ─── Create Teacher Portal User ───────────────────────────

    @http.route('/api/admin/teachers/<int:teacher_id>/create-portal-user', type='http',
                auth='none', methods=['POST', 'OPTIONS'], csrf=False, cors='*')
    @admin_jwt_required
    def create_teacher_portal_user(self, teacher_id, **kwargs):
        """Create portal user for a teacher. Auto-creates res.partner if needed."""
        data = get_request_data()
        t = request.env['education.employee'].sudo().browse(teacher_id)
        if not t.exists():
            return error_response('Teacher not found', 404, 'NOT_FOUND')

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return error_response('اسم المستخدم وكلمة المرور مطلوبان', 400, 'VALIDATION_ERROR')

        # Check if teacher already has a portal user via partner
        partner = None
        if hasattr(t, 'partner_id') and t.partner_id:
            partner = t.partner_id
        else:
            # Create a minimal res.partner for this teacher
            partner = request.env['res.partner'].sudo().create({
                'name': t.name,
                'phone': t.phone or '',
                'mobile': t.mobile or '',
                'email': t.email or '',
            })
            if hasattr(t, 'partner_id'):
                t.partner_id = partner.id

        # Check existing portal user
        existing = request.env['dar.portal.user'].sudo().search(
            [('partner_id', '=', partner.id)], limit=1)
        if existing:
            return error_response('يوجد حساب بالفعل لهذا المعلم', 400, 'ALREADY_EXISTS')

        try:
            import hashlib
            hashed = hashlib.sha256(password.encode()).hexdigest()
            pu = request.env['dar.portal.user'].sudo().create({
                'partner_id': partner.id,
                'username': username,
                'password_hash': hashed,
                'user_type': 'teacher',
                'is_active': True,
            })
            return json_response({
                'message': 'تم إنشاء حساب البوابة بنجاح',
                'portal_user': {
                    'id': pu.id,
                    'username': pu.username,
                    'user_type': pu.user_type,
                    'is_active': pu.is_active,
                },
            })
        except Exception as e:
            _logger.exception('Failed to create teacher portal user')
            return error_response(str(e), 500, 'CREATE_FAILED')

    # ─── Helper ──────────────────────────────────────────────

    def _get_portal_user_info(self, partner):
        """Get portal user info for a partner."""
        pu = request.env['dar.portal.user'].sudo().search(
            [('partner_id', '=', partner.id)], limit=1)
        if not pu:
            return None
        return {
            'id': pu.id,
            'username': pu.username,
            'user_type': pu.user_type,
            'is_active': pu.is_active,
            'last_login': str(pu.last_login) if pu.last_login else '',
            'login_count': pu.login_count,
        }
