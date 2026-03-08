# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date

GENDER_TYPES = [
    ('male', 'Male / ذكر'),
    ('female', 'Female / أنثى'),
]

PERIOD_TYPES = [
    ('morning', 'Morning / صباحي'),
    ('afternoon', 'Afternoon / مسائي'),
    ('full_day', 'Full Day / يوم كامل'),
]

STUDENT_STATES = [
    ('draft', 'Draft'),
    ('pending', 'Pending Enrollment'),
    ('enrolled', 'Enrolled'),
    ('suspended', 'Suspended'),
    ('archived', 'Archived'),
]

RELIGION_SELECTION = [
    ('islam', 'Islam'),
    ('christianity', 'Christianity'),
    ('other', 'Other'),
]

ADMISSION_TIME_SELECTION = [
    ('morning', 'Morning'),
    ('afternoon', 'Afternoon'),
    ('evening', 'Evening'),
]


class EducationStudent(models.Model):
    _inherit = 'res.partner'

    # Student flag
    is_student = fields.Boolean(
        string='Is Student',
        default=False,
        index=True,
    )

    # Basic Information (student-specific — name, phone, active, image_1920, country_id, street, comment already on res.partner)
    code = fields.Char(
        string='Student Code',
        readonly=True,
        copy=False,
        default='New',
    )
    arabic_name = fields.Char(
        string='Full Name (Arabic)',
        tracking=True,
    )
    birthdate = fields.Date(
        string='Birth Date',
        tracking=True,
    )
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    age_months = fields.Integer(
        string='Age (Months)',
        compute='_compute_age',
        store=True,
    )
    gender = fields.Selection(
        selection=GENDER_TYPES,
        string='Gender',
    )

    # PRD Gap Fields
    admission_time = fields.Selection(
        ADMISSION_TIME_SELECTION,
        string='Admission Time',
    )
    birth_order = fields.Integer(
        string='Birth Order',
    )
    religion = fields.Selection(
        RELIGION_SELECTION,
        string='Religion',
    )
    birth_place = fields.Char(
        string='Place of Birth',
    )

    # Parents (self-referential on res.partner)
    father_id = fields.Many2one(
        'res.partner',
        string='Father',
        domain="[('is_guardian', '=', True), ('guardian_relation', '=', 'father')]",
    )
    mother_id = fields.Many2one(
        'res.partner',
        string='Mother',
        domain="[('is_guardian', '=', True), ('guardian_relation', '=', 'mother')]",
    )

    # Academic Information
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        tracking=True,
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        domain="[('department_id', '=', department_id)]",
        tracking=True,
    )
    level_id = fields.Many2one(
        'education.level',
        string='Level',
        related='class_id.level_id',
        store=True,
        readonly=True,
    )
    academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Academic Year',
        domain="[('is_current', '=', True)]",
    )

    # Enrollment
    enrollment_date = fields.Date(
        string='Enrollment Date',
        default=fields.Date.context_today,
        tracking=True,
    )
    enrollment_source_id = fields.Many2one(
        'education.enrollment.source',
        string='Enrollment Source',
    )
    period = fields.Selection(
        selection=PERIOD_TYPES,
        string='Period',
        default='morning',
    )
    branch_id = fields.Many2one(
        'education.branch',
        string='Branch',
    )

    # Contact (student-specific — renamed from city_id to avoid conflict with partner's city char)
    student_city_id = fields.Many2one(
        'education.city',
        string='City',
    )

    # Health
    blood_type = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'),
        ('b+', 'B+'), ('b-', 'B-'),
        ('ab+', 'AB+'), ('ab-', 'AB-'),
        ('o+', 'O+'), ('o-', 'O-'),
    ], string='Blood Type')
    allergies = fields.Text(
        string='Allergies',
    )
    medical_notes = fields.Text(
        string='Medical Notes',
    )

    # State (renamed from state to student_state to avoid conflict)
    student_state = fields.Selection(
        selection=STUDENT_STATES,
        string='Student Status',
        default='draft',
        tracking=True,
    )

    # Related records
    sibling_ids = fields.One2many(
        'education.sibling',
        'student_id',
        string='Siblings',
    )
    authorized_pickup_ids = fields.One2many(
        'education.authorized.pickup',
        'student_id',
        string='Authorized Pickup',
    )
    student_note_ids = fields.One2many(
        'education.student.note',
        'student_id',
        string='Student Notes',
    )
    archive_ids = fields.One2many(
        'education.student.archive',
        'student_id',
        string='Archive History',
    )
    subscription_ids = fields.One2many(
        'education.student.subscription',
        'student_id',
        string='Subscriptions',
    )
    attendance_line_ids = fields.One2many(
        'education.attendance.line',
        'student_id',
        string='Attendance Records',
    )
    evaluation_ids = fields.One2many(
        'education.student.evaluation',
        'student_id',
        string='Evaluations',
    )
    homework_ids = fields.One2many(
        'education.student.homework',
        'student_id',
        string='Homework Submissions',
    )
    transport_ids = fields.One2many(
        'education.student.transport',
        'student_id',
        string='Transport',
    )
    study_plan_ids = fields.One2many(
        'education.study.plan',
        'student_id',
        string='Study Plans',
    )
    financial_plan_ids = fields.One2many(
        'education.financial.plan',
        'student_id',
        string='Financial Plans',
    )

    # Student-only computed counts (non-overlapping with guardian counts)
    attendance_count = fields.Integer(
        string='Attendance',
        compute='_compute_student_stat_counts',
    )
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_student_stat_counts',
    )
    homework_count = fields.Integer(
        string='Homework',
        compute='_compute_student_stat_counts',
    )
    stock_out_count = fields.Integer(
        string='Stock Out',
        compute='_compute_student_stat_counts',
    )
    student_message_count = fields.Integer(
        string='Messages',
        compute='_compute_student_stat_counts',
    )
    receipt_count = fields.Integer(
        string='Receipts',
        compute='_compute_student_stat_counts',
    )
    sibling_count = fields.Integer(
        string='Siblings',
        compute='_compute_student_stat_counts',
    )
    student_note_count = fields.Integer(
        string='Notes',
        compute='_compute_student_stat_counts',
    )
    study_plan_count = fields.Integer(
        compute='_compute_student_stat_counts',
        string='Study Plans',
    )
    financial_plan_count = fields.Integer(
        compute='_compute_student_stat_counts',
        string='Financial Plans',
    )

    # Computed fields from enhancements
    balance_due = fields.Float(
        compute='_compute_balance_due',
        string='Balance Due',
        store=True,
    )
    installment_count = fields.Integer(
        compute='_compute_installment_count',
        string='Installments',
    )
    goal_count = fields.Integer(
        compute='_compute_goal_count',
        string='Goals',
    )
    attendance_rate = fields.Float(
        compute='_compute_attendance_rate',
        string='Attendance Rate (%)',
    )

    @api.depends('birthdate')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birthdate:
                delta = relativedelta(today, record.birthdate)
                record.age = f"{delta.years} years, {delta.months} months"
                record.age_months = delta.years * 12 + delta.months
            else:
                record.age = ''
                record.age_months = 0

    def _compute_guardian_counts(self):
        """Extend guardian counts to also handle student-specific values."""
        super()._compute_guardian_counts()
        for record in self:
            if record.is_student:
                record.subscription_count = len(record.subscription_ids)
                installment_ids = record.subscription_ids.mapped('installment_ids').ids
                record.payment_count = self.env['education.payment'].search_count([
                    ('installment_id', 'in', installment_ids)
                ])
                record.transport_count = len(record.transport_ids)

    def _compute_student_stat_counts(self):
        for record in self:
            if not record.is_student:
                record.attendance_count = 0
                record.evaluation_count = 0
                record.homework_count = 0
                record.stock_out_count = 0
                record.student_message_count = 0
                record.receipt_count = 0
                record.sibling_count = 0
                record.student_note_count = 0
                record.study_plan_count = 0
                record.financial_plan_count = 0
                continue

            record.attendance_count = len(record.attendance_line_ids)
            record.evaluation_count = len(record.evaluation_ids)
            record.homework_count = len(record.homework_ids)
            record.sibling_count = len(record.sibling_ids)
            record.student_note_count = len(record.student_note_ids)
            record.study_plan_count = len(record.study_plan_ids)
            record.financial_plan_count = len(record.financial_plan_ids)

            record.stock_out_count = self.env['education.stock.out'].search_count([
                ('student_id', '=', record.id)
            ])

            record.student_message_count = self.env['education.message'].search_count([
                '|', '|',
                ('recipient_type', '=', 'all'),
                '&', ('recipient_type', '=', 'class'), ('class_id', '=', record.class_id.id),
                '&', ('recipient_type', '=', 'individual'), ('student_ids', 'in', record.id),
            ])

            record.receipt_count = self.env['education.payment.receipt'].search_count([
                ('student_id', '=', record.id)
            ])

    @api.depends('subscription_ids.total_amount', 'subscription_ids.status')
    def _compute_balance_due(self):
        for student in self:
            if not student.is_student:
                student.balance_due = 0.0
                continue
            total_due = 0.0
            for sub in student.subscription_ids.filtered(
                    lambda s: s.status == 'active'):
                for inst in sub.installment_ids:
                    if not inst.is_paid:
                        total_due += inst.amount - inst.paid_amount
            student.balance_due = total_due

    def _compute_installment_count(self):
        for student in self:
            if not student.is_student:
                student.installment_count = 0
                continue
            student.installment_count = self.env['education.installment'].search_count(
                [('subscription_id.student_id', '=', student.id)])

    def _compute_goal_count(self):
        for student in self:
            if not student.is_student:
                student.goal_count = 0
                continue
            student.goal_count = self.env['education.student.evaluation'].search_count(
                [('student_id', '=', student.id)])

    def _compute_attendance_rate(self):
        for student in self:
            if not student.is_student:
                student.attendance_rate = 0.0
                continue
            total = self.env['education.attendance.line'].search_count(
                [('student_id', '=', student.id)])
            present = self.env['education.attendance.line'].search_count(
                [('student_id', '=', student.id),
                 ('status', 'in', ['present', 'late'])])
            student.attendance_rate = (present / total * 100) if total else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_student'):
                if vals.get('code', 'New') == 'New':
                    vals['code'] = self.env['ir.sequence'].next_by_code('education.student') or 'New'
        return super().create(vals_list)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Clear class when department changes"""
        if self.department_id:
            if self.class_id and self.class_id.department_id != self.department_id:
                self.class_id = False
        else:
            self.class_id = False

    @api.onchange('id_number')
    def _onchange_id_number_student(self):
        """Auto-detect guardian by national ID."""
        if self.is_student and self.id_number:
            parent = self.env['res.partner'].search(
                [('is_guardian', '=', True),
                 ('id_number', '=', self.id_number)], limit=1)
            if parent and not self.father_id and parent.guardian_relation == 'father':
                self.father_id = parent.id
            elif parent and not self.mother_id and parent.guardian_relation == 'mother':
                self.mother_id = parent.id

    def action_pending(self):
        """Set to pending enrollment"""
        self.write({'student_state': 'pending'})

    def action_enroll(self):
        """Enroll the student"""
        self.write({'student_state': 'enrolled'})

    def action_suspend(self):
        """Suspend the student"""
        self.write({'student_state': 'suspended'})

    def action_archive_student(self):
        """Archive the student"""
        self.write({'student_state': 'archived', 'active': False})

    def action_reactivate(self):
        """Reactivate archived student"""
        self.write({'student_state': 'enrolled', 'active': True})

    # Stat button actions
    def action_view_subscriptions(self):
        """View student subscriptions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_attendance(self):
        """View student attendance records"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance',
            'res_model': 'education.attendance.line',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }

    def action_view_evaluations(self):
        """View student evaluations"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations',
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_homework(self):
        """View student homework submissions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'education.student.homework',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }

    def action_view_transport(self):
        """View student transport assignment"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transport',
            'res_model': 'education.student.transport',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_payments(self):
        """View student payments"""
        self.ensure_one()
        if self.is_student:
            installment_ids = self.subscription_ids.mapped('installment_ids').ids
            return {
                'type': 'ir.actions.act_window',
                'name': 'Payments',
                'res_model': 'education.payment',
                'view_mode': 'list,form',
                'domain': [('installment_id', 'in', installment_ids)],
            }
        return super().action_view_payments()

    def action_view_stock_out(self):
        """View stock out records for this student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Out',
            'res_model': 'education.stock.out',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_messages(self):
        """View messages sent to this student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Messages',
            'res_model': 'education.message',
            'view_mode': 'list,form',
            'domain': [
                '|', '|',
                ('recipient_type', '=', 'all'),
                '&', ('recipient_type', '=', 'class'), ('class_id', '=', self.class_id.id),
                '&', ('recipient_type', '=', 'individual'), ('student_ids', 'in', self.id),
            ],
        }

    def action_view_receipts(self):
        """View payment receipts for this student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Receipts',
            'res_model': 'education.payment.receipt',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_siblings(self):
        """View student siblings"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Siblings',
            'res_model': 'education.sibling',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_notes(self):
        """View student notes"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Notes',
            'res_model': 'education.student.note',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_father(self):
        """View student's father"""
        self.ensure_one()
        if self.father_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Father',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.father_id.id,
            }

    def action_view_mother(self):
        """View student's mother"""
        self.ensure_one()
        if self.mother_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Mother',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': self.mother_id.id,
            }

    # Smart button actions (from enhancements)
    def action_view_balance(self):
        """View unpaid installments (balance due)"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Balance Due'),
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id.student_id', '=', self.id),
                        ('is_paid', '=', False)],
            'context': {'default_student_id': self.id},
        }

    def action_view_account_statement(self):
        """View account statement for this student"""
        self.ensure_one()
        if self.is_student:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Account Statement'),
                'res_model': 'education.payment',
                'view_mode': 'list,form',
                'domain': [('installment_id.subscription_id.student_id', '=', self.id)],
            }
        return super().action_view_account_statement()

    def action_view_installments(self):
        """View all installments for this student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Installments'),
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id.student_id', '=', self.id)],
        }

    def action_view_goals(self):
        """View goals and assessments for this student"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Goals & Assessments'),
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }
