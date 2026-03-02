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
    _name = 'education.student'
    _description = 'Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'code, name'

    # Basic Information
    code = fields.Char(
        string='Student Code',
        readonly=True,
        copy=False,
        default='New',
    )
    name = fields.Char(
        string='Full Name (English)',
        required=True,
        tracking=True,
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
        required=True,
        default='male',
    )
    photo = fields.Binary(
        string='Photo',
        attachment=True,
    )
    nationality = fields.Many2one(
        'res.country',
        string='Nationality',
    )

    # PRD Gap Fields (from new enhancements)
    national_id = fields.Char(
        string='National ID / Iqama',
    )
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

    # Parents
    father_id = fields.Many2one(
        'education.parent',
        string='Father',
        domain="[('relation', '=', 'father')]",
    )
    mother_id = fields.Many2one(
        'education.parent',
        string='Mother',
        domain="[('relation', '=', 'mother')]",
    )

    # Academic Information
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
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

    # Contact
    phone = fields.Char(
        string='Phone',
    )
    address = fields.Text(
        string='Address',
    )
    city_id = fields.Many2one(
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

    # State
    state = fields.Selection(
        selection=STUDENT_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    notes = fields.Text(
        string='Notes',
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
    note_ids = fields.One2many(
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

    # Computed counts for stat buttons (original)
    subscription_count = fields.Integer(
        string='Subscriptions',
        compute='_compute_stat_counts',
    )
    attendance_count = fields.Integer(
        string='Attendance',
        compute='_compute_stat_counts',
    )
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_stat_counts',
    )
    homework_count = fields.Integer(
        string='Homework',
        compute='_compute_stat_counts',
    )
    transport_count = fields.Integer(
        string='Transport',
        compute='_compute_stat_counts',
    )
    payment_count = fields.Integer(
        string='Payments',
        compute='_compute_stat_counts',
    )
    stock_out_count = fields.Integer(
        string='Stock Out',
        compute='_compute_stat_counts',
    )
    message_count = fields.Integer(
        string='Messages',
        compute='_compute_stat_counts',
    )
    receipt_count = fields.Integer(
        string='Receipts',
        compute='_compute_stat_counts',
    )
    sibling_count = fields.Integer(
        string='Siblings',
        compute='_compute_stat_counts',
    )
    note_count = fields.Integer(
        string='Notes',
        compute='_compute_stat_counts',
    )

    # Computed fields from new enhancements
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

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Student code must be unique!'),
    ]

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

    def _compute_stat_counts(self):
        for record in self:
            record.subscription_count = len(record.subscription_ids)
            record.attendance_count = len(record.attendance_line_ids)
            record.evaluation_count = len(record.evaluation_ids)
            record.homework_count = len(record.homework_ids)
            record.transport_count = len(record.transport_ids)
            record.sibling_count = len(record.sibling_ids)
            record.note_count = len(record.note_ids)

            # Count payments from all subscriptions
            installment_ids = record.subscription_ids.mapped('installment_ids').ids
            record.payment_count = self.env['education.payment'].search_count([
                ('installment_id', 'in', installment_ids)
            ])

            # Stock out records for this student
            record.stock_out_count = self.env['education.stock.out'].search_count([
                ('student_id', '=', record.id)
            ])

            # Messages sent to this student (via class or individual)
            record.message_count = self.env['education.message'].search_count([
                '|', '|',
                ('recipient_type', '=', 'all'),
                '&', ('recipient_type', '=', 'class'), ('class_id', '=', record.class_id.id),
                '&', ('recipient_type', '=', 'individual'), ('student_ids', 'in', record.id),
            ])

            # Payment receipts for this student
            record.receipt_count = self.env['education.payment.receipt'].search_count([
                ('student_id', '=', record.id)
            ])

    @api.depends('subscription_ids.total_amount', 'subscription_ids.status')
    def _compute_balance_due(self):
        for student in self:
            total_due = 0.0
            for sub in student.subscription_ids.filtered(
                    lambda s: s.status == 'active'):
                for inst in sub.installment_ids:
                    if not inst.is_paid:
                        total_due += inst.amount - inst.paid_amount
            student.balance_due = total_due

    def _compute_installment_count(self):
        for student in self:
            student.installment_count = self.env['education.installment'].search_count(
                [('subscription_id.student_id', '=', student.id)])

    def _compute_goal_count(self):
        for student in self:
            student.goal_count = self.env['education.student.evaluation'].search_count(
                [('student_id', '=', student.id)])

    def _compute_attendance_rate(self):
        for student in self:
            total = self.env['education.attendance.line'].search_count(
                [('student_id', '=', student.id)])
            present = self.env['education.attendance.line'].search_count(
                [('student_id', '=', student.id),
                 ('status', 'in', ['present', 'late'])])
            student.attendance_rate = (present / total * 100) if total else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
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

    @api.onchange('national_id')
    def _onchange_national_id(self):
        """Auto-detect guardian by national ID."""
        if self.national_id:
            parent = self.env['education.parent'].search(
                [('id_number', '=', self.national_id)], limit=1)
            if parent and not self.father_id and parent.relation == 'father':
                self.father_id = parent.id
            elif parent and not self.mother_id and parent.relation == 'mother':
                self.mother_id = parent.id

    def action_pending(self):
        """Set to pending enrollment"""
        self.write({'state': 'pending'})

    def action_enroll(self):
        """Enroll the student"""
        self.write({'state': 'enrolled'})

    def action_suspend(self):
        """Suspend the student"""
        self.write({'state': 'suspended'})

    def action_archive_student(self):
        """Archive the student"""
        self.write({'state': 'archived', 'active': False})

    def action_reactivate(self):
        """Reactivate archived student"""
        self.write({'state': 'enrolled', 'active': True})

    # Stat button actions (original)
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
        installment_ids = self.subscription_ids.mapped('installment_ids').ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('installment_id', 'in', installment_ids)],
        }

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
                'res_model': 'education.parent',
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
                'res_model': 'education.parent',
                'view_mode': 'form',
                'res_id': self.mother_id.id,
            }

    # Smart button actions (from new enhancements)
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
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Statement'),
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('installment_id.subscription_id.student_id', '=', self.id)],
        }

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
