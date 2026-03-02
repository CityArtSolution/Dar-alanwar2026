# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

RELATION_TYPES = [
    ('father', 'Father / أب'),
    ('mother', 'Mother / أم'),
    ('guardian', 'Guardian / ولي أمر'),
    ('grandfather', 'Grandfather / جد'),
    ('grandmother', 'Grandmother / جدة'),
    ('uncle', 'Uncle / عم أو خال'),
    ('aunt', 'Aunt / عمة أو خالة'),
    ('other', 'Other / آخر'),
]

MARITAL_STATUS = [
    ('married', 'Married / متزوج'),
    ('divorced', 'Divorced / مطلق'),
    ('widowed', 'Widowed / أرمل'),
    ('single', 'Single / أعزب'),
]

EDUCATION_LEVELS = [
    ('primary', 'Primary'),
    ('secondary', 'Secondary'),
    ('diploma', 'Diploma'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('phd', 'PhD'),
]


class EducationParent(models.Model):
    _name = 'education.parent'
    _description = 'Parent / Guardian'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(
        string='Full Name',
        required=True,
        tracking=True,
    )
    phone = fields.Char(
        string='Phone',
        tracking=True,
    )
    mobile = fields.Char(
        string='Mobile',
        tracking=True,
    )
    email = fields.Char(
        string='Email',
    )
    job = fields.Char(
        string='Job / Occupation',
    )
    workplace = fields.Char(
        string='Workplace',
    )
    relation = fields.Selection(
        selection=RELATION_TYPES,
        string='Relation Type',
        required=True,
        default='father',
    )
    marital_status = fields.Selection(
        selection=MARITAL_STATUS,
        string='Marital Status',
    )
    address = fields.Text(
        string='Address',
    )
    city_id = fields.Many2one(
        'education.city',
        string='City',
    )
    id_number = fields.Char(
        string='ID Number',
    )
    photo = fields.Binary(
        string='Photo',
        attachment=True,
    )
    notes = fields.Text(
        string='Notes',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # PRD Gap Fields (from new enhancements)
    nationality = fields.Many2one(
        'res.country',
        string='Nationality',
    )
    job_number = fields.Char(
        string='Job/Employee Number',
    )
    education_level = fields.Selection(
        EDUCATION_LEVELS,
        string='Education Level',
    )
    mother_name = fields.Char(
        string='Mother Full Name',
    )
    mother_phone = fields.Char(
        string='Mother Phone',
    )
    mother_national_id = fields.Char(
        string='Mother National ID',
    )
    mother_education = fields.Selection(
        EDUCATION_LEVELS,
        string='Mother Education Level',
    )

    # Related children
    father_student_ids = fields.One2many(
        'education.student',
        'father_id',
        string='Children (as Father)',
    )
    mother_student_ids = fields.One2many(
        'education.student',
        'mother_id',
        string='Children (as Mother)',
    )

    # Computed counts (original)
    student_count = fields.Integer(
        string='Student Count',
        compute='_compute_counts',
    )
    subscription_count = fields.Integer(
        string='Subscription Count',
        compute='_compute_counts',
    )
    payment_count = fields.Integer(
        string='Payment Count',
        compute='_compute_counts',
    )
    message_count = fields.Integer(
        string='Message Count',
        compute='_compute_counts',
    )
    transport_count = fields.Integer(
        string='Transport Count',
        compute='_compute_counts',
    )
    total_paid = fields.Float(
        string='Total Paid',
        compute='_compute_counts',
    )
    total_remaining = fields.Float(
        string='Total Remaining',
        compute='_compute_counts',
    )

    # Computed fields from new enhancements
    children_count = fields.Integer(
        compute='_compute_children_stats',
        string='Children',
    )
    children_invoice_count = fields.Integer(
        compute='_compute_children_stats',
        string='Invoices',
    )
    children_balance_due = fields.Float(
        compute='_compute_children_stats',
        string='Balance Due',
    )
    children_installment_count = fields.Integer(
        compute='_compute_children_stats',
        string='Installments',
    )
    children_attendance_pct = fields.Float(
        compute='_compute_children_stats',
        string='Attendance %',
    )

    @api.depends('father_student_ids', 'mother_student_ids')
    def _compute_counts(self):
        for record in self:
            student_ids = record.father_student_ids.ids + record.mother_student_ids.ids
            record.student_count = len(student_ids)

            if student_ids:
                # Count subscriptions
                subscriptions = self.env['education.student.subscription'].search([
                    ('student_id', 'in', student_ids)
                ])
                record.subscription_count = len(subscriptions)
                record.total_paid = sum(subscriptions.mapped('paid_amount'))
                record.total_remaining = sum(subscriptions.mapped('remaining_amount'))

                # Count payments
                record.payment_count = self.env['education.payment'].search_count([
                    ('student_id', 'in', student_ids)
                ])

                # Count messages
                record.message_count = self.env['education.message'].search_count([
                    ('student_ids', 'in', student_ids)
                ])

                # Count transport
                record.transport_count = self.env['education.student.transport'].search_count([
                    ('student_id', 'in', student_ids)
                ])
            else:
                record.subscription_count = 0
                record.payment_count = 0
                record.message_count = 0
                record.transport_count = 0
                record.total_paid = 0.0
                record.total_remaining = 0.0

    def _get_student_ids(self):
        """Helper to get all student IDs for this parent"""
        self.ensure_one()
        return self.father_student_ids.ids + self.mother_student_ids.ids

    def _get_all_children(self):
        """Helper to get all children recordset for this parent"""
        self.ensure_one()
        return self.father_student_ids | self.mother_student_ids

    @api.depends('father_student_ids', 'mother_student_ids')
    def _compute_children_stats(self):
        for parent in self:
            children = parent._get_all_children()
            parent.children_count = len(children)

            # Installments
            installments = self.env['education.installment'].search([
                ('subscription_id.student_id', 'in', children.ids)])
            parent.children_installment_count = len(installments)

            # Balance due
            unpaid = installments.filtered(lambda i: not i.is_paid)
            parent.children_balance_due = sum(
                i.amount - i.paid_amount for i in unpaid)

            # Invoice count (payment receipts)
            parent.children_invoice_count = self.env[
                'education.payment.receipt'].search_count(
                [('student_id', 'in', children.ids)])

            # Attendance percentage
            total_att = self.env['education.attendance.line'].search_count(
                [('student_id', 'in', children.ids)])
            present_att = self.env['education.attendance.line'].search_count(
                [('student_id', 'in', children.ids),
                 ('status', 'in', ['present', 'late'])])
            parent.children_attendance_pct = (
                (present_att / total_att * 100) if total_att else 0.0)

    # Stat button actions (original)
    def action_view_students(self):
        """View parent's children"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Children',
            'res_model': 'education.student',
            'view_mode': 'list,kanban,form',
            'domain': [('id', 'in', self._get_student_ids())],
        }

    def action_view_subscriptions(self):
        """View subscriptions for all children"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subscriptions',
            'res_model': 'education.student.subscription',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', self._get_student_ids())],
        }

    def action_view_payments(self):
        """View payments for all children"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', self._get_student_ids())],
        }

    def action_view_messages(self):
        """View messages sent to this parent's children"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Messages',
            'res_model': 'education.message',
            'view_mode': 'list,form',
            'domain': [('student_ids', 'in', self._get_student_ids())],
        }

    def action_view_transport(self):
        """View transport for all children"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transport',
            'res_model': 'education.student.transport',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', self._get_student_ids())],
        }

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.relation:
                relation_label = dict(RELATION_TYPES).get(record.relation, '')
                name = f"{record.name} ({relation_label})"
            result.append((record.id, name))
        return result

    # Smart button actions (from new enhancements)
    def action_view_children_invoices(self):
        """View invoices/receipts for all children"""
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Children Invoices'),
            'res_model': 'education.payment.receipt',
            'view_mode': 'list,form',
            'domain': [('student_id', 'in', children.ids)],
        }

    def action_view_children_balance(self):
        """View unpaid installments for all children"""
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Unpaid Installments'),
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id.student_id', 'in', children.ids),
                        ('is_paid', '=', False)],
        }

    def action_view_children_installments(self):
        """View all installments for all children"""
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('All Installments'),
            'res_model': 'education.installment',
            'view_mode': 'list,form',
            'domain': [('subscription_id.student_id', 'in', children.ids)],
        }

    def action_view_account_statement(self):
        """View account statement for all children"""
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Statement'),
            'res_model': 'education.payment',
            'view_mode': 'list,form',
            'domain': [
                ('installment_id.subscription_id.student_id', 'in', children.ids)],
        }

    def action_view_children_attendance(self):
        """View attendance records for all children"""
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Children Attendance'),
            'res_model': 'education.attendance.line',
            'view_mode': 'list',
            'domain': [('student_id', 'in', children.ids)],
        }
