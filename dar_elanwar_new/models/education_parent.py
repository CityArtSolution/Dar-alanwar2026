from odoo import models, fields, api, _


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
    _description = 'Guardian / Parent'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    email = fields.Char(string='Email')
    job = fields.Char(string='Job Title')
    workplace = fields.Char(string='Workplace')
    relation = fields.Selection([
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ], string='Relation', required=True, default='father')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ], string='Marital Status')
    id_number = fields.Char(string='National ID / Iqama')
    photo = fields.Binary(string='Photo', attachment=True)
    active = fields.Boolean(default=True)

    # PRD Gap Fields
    nationality = fields.Many2one('res.country', string='Nationality')
    job_number = fields.Char(string='Job/Employee Number')
    education_level = fields.Selection(EDUCATION_LEVELS, string='Education Level')
    mother_name = fields.Char(string='Mother Full Name')
    mother_phone = fields.Char(string='Mother Phone')
    mother_national_id = fields.Char(string='Mother National ID')
    mother_education = fields.Selection(EDUCATION_LEVELS,
                                         string='Mother Education Level')

    # Related Children
    father_student_ids = fields.One2many('education.student', 'father_id',
                                          string='Children (Father)')
    mother_student_ids = fields.One2many('education.student', 'mother_id',
                                          string='Children (Mother)')

    # Computed Fields for Smart Buttons
    children_count = fields.Integer(compute='_compute_children_stats',
                                      string='Children')
    children_invoice_count = fields.Integer(compute='_compute_children_stats',
                                              string='Invoices')
    children_balance_due = fields.Float(compute='_compute_children_stats',
                                          string='Balance Due')
    children_installment_count = fields.Integer(compute='_compute_children_stats',
                                                  string='Installments')
    children_attendance_pct = fields.Float(compute='_compute_children_stats',
                                            string='Attendance %')

    def _get_all_children(self):
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

    # Smart Button Actions
    def action_view_children_invoices(self):
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
        self.ensure_one()
        children = self._get_all_children()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Children Attendance'),
            'res_model': 'education.attendance.line',
            'view_mode': 'list',
            'domain': [('student_id', 'in', children.ids)],
        }
