from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


SUBSCRIPTION_STATUS = [
    ('draft', 'Draft'),
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class EducationStudentSubscription(models.Model):
    _name = 'education.student.subscription'
    _description = 'Student Subscription'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    student_id = fields.Many2one('education.student', string='Student',
                                  required=True, tracking=True)
    type_id = fields.Many2one('education.subscription.type',
                               string='Subscription Type', required=True)
    plan_id = fields.Many2one('education.payment.plan', string='Payment Plan')
    academic_year_id = fields.Many2one('education.academic.year',
                                        string='Academic Year')

    total_amount = fields.Float(string='Total Amount')
    discount_id = fields.Many2one('education.discount', string='Discount Applied')
    discount_type = fields.Selection([
        ('sibling', 'Sibling'),
        ('early_payment', 'Early Payment'),
        ('scholarship', 'Scholarship'),
        ('custom', 'Custom'),
    ], string='Discount Type', related='discount_id.discount_type', store=True)
    discount_amount = fields.Float(string='Discount Amount',
                                     compute='_compute_discount_amount', store=True)
    net_amount = fields.Float(string='Net Amount',
                               compute='_compute_net_amount', store=True)

    status = fields.Selection(SUBSCRIPTION_STATUS, string='Status',
                               default='draft', tracking=True)

    installment_ids = fields.One2many('education.installment', 'subscription_id',
                                       string='Installments')
    paid_amount = fields.Float(compute='_compute_paid_amount', string='Paid',
                                store=True)
    remaining_amount = fields.Float(compute='_compute_paid_amount',
                                      string='Remaining', store=True)

    @api.depends('total_amount', 'discount_id', 'discount_id.value',
                 'discount_id.value_type')
    def _compute_discount_amount(self):
        for rec in self:
            if rec.discount_id:
                if rec.discount_id.value_type == 'percentage':
                    rec.discount_amount = rec.total_amount * rec.discount_id.value / 100
                else:
                    rec.discount_amount = rec.discount_id.value
            else:
                rec.discount_amount = 0.0

    @api.depends('total_amount', 'discount_amount')
    def _compute_net_amount(self):
        for rec in self:
            rec.net_amount = rec.total_amount - rec.discount_amount

    @api.depends('installment_ids.paid_amount', 'installment_ids.is_paid',
                 'net_amount')
    def _compute_paid_amount(self):
        for rec in self:
            rec.paid_amount = sum(rec.installment_ids.mapped('paid_amount'))
            rec.remaining_amount = rec.net_amount - rec.paid_amount

    @api.onchange('type_id')
    def _onchange_type_id(self):
        if self.type_id:
            self.total_amount = self.type_id.amount
            if self.type_id.payment_plan_id:
                self.plan_id = self.type_id.payment_plan_id

    def action_activate(self):
        self.write({'status': 'active'})

    def action_complete(self):
        self.write({'status': 'completed'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_generate_installments(self):
        """Generate installment records based on payment plan."""
        for sub in self:
            if not sub.plan_id:
                continue
            sub.installment_ids.unlink()
            amount_per_inst = sub.net_amount / sub.plan_id.installment_count
            start_date = fields.Date.today()
            for i in range(sub.plan_id.installment_count):
                due_date = start_date + relativedelta(
                    months=i * sub.plan_id.interval_months)
                self.env['education.installment'].create({
                    'subscription_id': sub.id,
                    'sequence': i + 1,
                    'due_date': due_date,
                    'amount': amount_per_inst,
                })

    @api.model
    def _cron_auto_generate_invoices(self):
        """Cron job to auto-create draft invoices from active subscriptions."""
        active_subs = self.search([('status', '=', 'active')])
        for sub in active_subs:
            overdue = sub.installment_ids.filtered(
                lambda i: not i.is_paid and i.due_date <= fields.Date.today())
            for inst in overdue:
                existing = self.env['education.payment.receipt'].search([
                    ('student_id', '=', sub.student_id.id),
                    ('installment_id', '=', inst.id),
                ], limit=1)
                if not existing:
                    self.env['education.payment.receipt'].create({
                        'student_id': sub.student_id.id,
                        'date': fields.Date.today(),
                        'total_amount': inst.amount - inst.paid_amount,
                        'installment_id': inst.id,
                    })

    def _auto_apply_sibling_discount(self):
        """Auto-apply sibling discount when enrolling students with same parent."""
        for sub in self:
            student = sub.student_id
            parent = student.father_id or student.mother_id
            if not parent:
                continue
            siblings = parent._get_all_children().filtered(
                lambda s: s.id != student.id and s.state == 'enrolled')
            if len(siblings) >= 1:
                sibling_discount = self.env['education.discount'].search([
                    ('discount_type', '=', 'sibling'),
                    ('auto_apply', '=', True),
                    ('active', '=', True),
                    '|',
                    ('department_id', '=', False),
                    ('department_id', '=', student.department_id.id),
                ], limit=1)
                if sibling_discount and not sub.discount_id:
                    sub.discount_id = sibling_discount.id
