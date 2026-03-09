from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


STUDENT_STATES = [
    ('draft', 'Draft'),
    ('pending', 'Pending'),
    ('enrolled', 'Enrolled'),
    ('suspended', 'Suspended'),
    ('archived', 'Archived'),
]

GENDER_SELECTION = [
    ('male', 'Male'),
    ('female', 'Female'),
]

BLOOD_TYPES = [
    ('a+', 'A+'), ('a-', 'A-'),
    ('b+', 'B+'), ('b-', 'B-'),
    ('ab+', 'AB+'), ('ab-', 'AB-'),
    ('o+', 'O+'), ('o-', 'O-'),
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
    _order = 'code'

    # Basic Info
    code = fields.Char(string='Student Code', readonly=True, copy=False,
                       default=lambda self: _('New'))
    name = fields.Char(string='Name (English)', required=True, tracking=True)
    arabic_name = fields.Char(string='Name (Arabic)')
    photo = fields.Binary(string='Photo', attachment=True)
    birthdate = fields.Date(string='Date of Birth')
    gender = fields.Selection(GENDER_SELECTION, string='Gender')
    nationality = fields.Many2one('res.country', string='Nationality')

    # PRD Gap Fields
    national_id = fields.Char(string='National ID / Iqama')
    admission_time = fields.Selection(ADMISSION_TIME_SELECTION,
                                       string='Admission Time')
    birth_order = fields.Integer(string='Birth Order')
    religion = fields.Selection(RELIGION_SELECTION, string='Religion')
    birth_place = fields.Char(string='Place of Birth')

    # Guardians
    father_id = fields.Many2one('education.parent', string='Father',
                                 domain=[('relation', '=', 'father')])
    mother_id = fields.Many2one('education.parent', string='Mother',
                                 domain=[('relation', '=', 'mother')])

    # Academic
    department_id = fields.Many2one('education.department', string='Department',
                                     tracking=True)
    class_id = fields.Many2one('education.class', string='Class',
                                domain="[('department_id', '=', department_id)]",
                                tracking=True)
    level_id = fields.Many2one('education.level', string='Level',
                                related='class_id.level_id', store=True)
    enrollment_date = fields.Date(string='Enrollment Date')
    period = fields.Selection([
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
        ('full', 'Full Year'),
    ], string='Period', default='full')
    academic_year_id = fields.Many2one('education.academic.year',
                                        string='Academic Year')
    source_id = fields.Many2one('education.enrollment.source',
                                 string='Enrollment Source')

    # Branch
    branch_id = fields.Many2one('education.branch', string='Branch')

    # Medical
    blood_type = fields.Selection(BLOOD_TYPES, string='Blood Type')
    allergies = fields.Text(string='Allergies')
    medical_notes = fields.Text(string='Medical Notes')

    # Status
    state = fields.Selection(STUDENT_STATES, string='Status', default='draft',
                              tracking=True)

    # Related Records
    sibling_ids = fields.One2many('education.sibling', 'student_id',
                                   string='Siblings')
    note_ids = fields.One2many('education.student.note', 'student_id',
                                string='Notes')
    archive_ids = fields.One2many('education.student.archive', 'student_id',
                                   string='Archive History')
    authorized_pickup_ids = fields.One2many('education.authorized.pickup',
                                             'student_id',
                                             string='Authorized Pickup')
    subscription_ids = fields.One2many('education.student.subscription',
                                        'student_id', string='Subscriptions')
    attendance_line_ids = fields.One2many('education.attendance.line',
                                           'student_id', string='Attendance')

    # Computed Fields for Smart Buttons
    balance_due = fields.Float(compute='_compute_balance_due',
                                string='Balance Due', store=True)
    installment_count = fields.Integer(compute='_compute_installment_count',
                                        string='Installments')
    goal_count = fields.Integer(compute='_compute_goal_count',
                                 string='Goals')
    attendance_rate = fields.Float(compute='_compute_attendance_rate',
                                    string='Attendance Rate (%)')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Student code must be unique!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', _('New')) == _('New'):
                prefix = self.env['ir.config_parameter'].sudo().get_param(
                    'dar_elanwar.student_code_prefix', 'STD')
                vals['code'] = self.env['ir.sequence'].next_by_code(
                    'education.student') or _('New')
        return super().create(vals_list)

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

    # State transitions
    def action_submit(self):
        self.write({'state': 'pending'})

    def action_enroll(self):
        self.write({'state': 'enrolled'})

    def action_suspend(self):
        self.write({'state': 'suspended'})

    def action_archive_student(self):
        self.write({'state': 'archived'})

    def action_reactivate(self):
        self.write({'state': 'enrolled'})

    # Smart Button Actions
    def action_view_balance(self):
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
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Statement'),
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('installment_id.subscription_id.student_id', '=', self.id)],
        }

    def action_view_installments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Installments'),
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id.student_id', '=', self.id)],
        }

    def action_view_goals(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Goals & Assessments'),
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
        }
