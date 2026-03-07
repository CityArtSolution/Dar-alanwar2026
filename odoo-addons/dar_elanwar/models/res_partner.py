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

SOCIAL_STATUS = [
    ('married', 'Married / متزوج'),
    ('divorced', 'Divorced / مطلق'),
    ('widowed', 'Widowed / أرمل'),
    ('separated', 'Separated / منفصل'),
]

EDUCATION_LEVELS = [
    ('primary', 'Primary'),
    ('preparatory', 'Preparatory'),
    ('secondary', 'Secondary'),
    ('university', 'University'),
    ('postgraduate', 'Postgraduate'),
    ('other', 'Other'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_guardian = fields.Boolean(
        string='Is Guardian',
        default=False,
        index=True,
    )
    guardian_relation = fields.Selection(
        selection=RELATION_TYPES,
        string='Relation Type',
    )
    parent_social_status = fields.Selection(
        selection=SOCIAL_STATUS,
        string='Social Status',
    )
    guardian_mobile = fields.Char(
        string='Mobile',
    )
    id_number = fields.Char(
        string='National ID',
    )
    workplace = fields.Char(
        string='Workplace',
    )
    job_number = fields.Char(
        string='Job/Employee Number',
    )
    education_level = fields.Selection(
        EDUCATION_LEVELS,
        string='Education Level',
    )
    guardian_city_id = fields.Many2one(
        'education.city',
        string='City',
    )

    # Mother information
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
        compute='_compute_guardian_counts',
    )
    subscription_count = fields.Integer(
        string='Subscription Count',
        compute='_compute_guardian_counts',
    )
    payment_count = fields.Integer(
        string='Payment Count',
        compute='_compute_guardian_counts',
    )
    guardian_message_count = fields.Integer(
        string='Message Count',
        compute='_compute_guardian_counts',
    )
    transport_count = fields.Integer(
        string='Transport Count',
        compute='_compute_guardian_counts',
    )
    total_paid = fields.Float(
        string='Total Paid',
        compute='_compute_guardian_counts',
    )
    total_remaining = fields.Float(
        string='Total Remaining',
        compute='_compute_guardian_counts',
    )

    # Computed fields from enhancements
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
    def _compute_guardian_counts(self):
        for record in self:
            if not record.is_guardian:
                record.student_count = 0
                record.subscription_count = 0
                record.payment_count = 0
                record.guardian_message_count = 0
                record.transport_count = 0
                record.total_paid = 0.0
                record.total_remaining = 0.0
                continue

            student_ids = record.father_student_ids.ids + record.mother_student_ids.ids
            record.student_count = len(student_ids)

            if student_ids:
                subscriptions = self.env['education.student.subscription'].search([
                    ('student_id', 'in', student_ids)
                ])
                record.subscription_count = len(subscriptions)
                record.total_paid = sum(subscriptions.mapped('paid_amount'))
                record.total_remaining = sum(subscriptions.mapped('remaining_amount'))

                record.payment_count = self.env['education.payment'].search_count([
                    ('student_id', 'in', student_ids)
                ])

                record.guardian_message_count = self.env['education.message'].search_count([
                    ('student_ids', 'in', student_ids)
                ])

                record.transport_count = self.env['education.student.transport'].search_count([
                    ('student_id', 'in', student_ids)
                ])
            else:
                record.subscription_count = 0
                record.payment_count = 0
                record.guardian_message_count = 0
                record.transport_count = 0
                record.total_paid = 0.0
                record.total_remaining = 0.0

    def _get_student_ids(self):
        """Helper to get all student IDs for this guardian"""
        self.ensure_one()
        return self.father_student_ids.ids + self.mother_student_ids.ids

    def _get_all_children(self):
        """Helper to get all children recordset for this guardian"""
        self.ensure_one()
        return self.father_student_ids | self.mother_student_ids

    @api.depends('father_student_ids', 'mother_student_ids')
    def _compute_children_stats(self):
        for partner in self:
            if not partner.is_guardian:
                partner.children_count = 0
                partner.children_installment_count = 0
                partner.children_balance_due = 0.0
                partner.children_invoice_count = 0
                partner.children_attendance_pct = 0.0
                continue

            children = partner._get_all_children()
            partner.children_count = len(children)

            # Installments
            installments = self.env['education.installment'].search([
                ('subscription_id.student_id', 'in', children.ids)])
            partner.children_installment_count = len(installments)

            # Balance due
            unpaid = installments.filtered(lambda i: not i.is_paid)
            partner.children_balance_due = sum(
                i.amount - i.paid_amount for i in unpaid)

            # Invoice count (payment receipts)
            partner.children_invoice_count = self.env[
                'education.payment.receipt'].search_count(
                [('student_id', 'in', children.ids)])

            # Attendance percentage
            total_att = self.env['education.attendance.line'].search_count(
                [('student_id', 'in', children.ids)])
            present_att = self.env['education.attendance.line'].search_count(
                [('student_id', 'in', children.ids),
                 ('status', 'in', ['present', 'late'])])
            partner.children_attendance_pct = (
                (present_att / total_att * 100) if total_att else 0.0)

    # Stat button actions (original)
    def action_view_students(self):
        """View guardian's children"""
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

    def action_view_guardian_messages(self):
        """View messages sent to this guardian's children"""
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
            if record.is_guardian and record.guardian_relation:
                relation_label = dict(RELATION_TYPES).get(
                    record.guardian_relation, '')
                name = f"{record.name} ({relation_label})"
                result.append((record.id, name))
            else:
                result.append((record.id, record.name or ''))
        return result

    # Smart button actions (from enhancements)
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
