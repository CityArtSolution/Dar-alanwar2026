from odoo import models, fields, api, _
import uuid
import base64


class EducationKidsAreaService(models.Model):
    _name = 'education.kids.area.service'
    _description = 'Kids Area Service'

    name = fields.Char(string='Service Name', required=True)
    activity_type = fields.Selection([
        ('play', 'Play'),
        ('learning', 'Learning'),
        ('craft', 'Craft'),
        ('sport', 'Sport'),
    ], string='Activity Type', required=True)
    pricing_type = fields.Selection([
        ('hourly', 'Hourly'),
        ('session', 'Per Session'),
        ('package', 'Package'),
    ], string='Pricing Type', default='session')
    price = fields.Float(string='Price')
    capacity = fields.Integer(string='Max Capacity', default=20)
    min_age = fields.Integer(string='Min Age')
    max_age = fields.Integer(string='Max Age')
    duration_minutes = fields.Integer(string='Duration (Minutes)', default=60)
    image = fields.Binary(string='Image', attachment=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)


class EducationKidsAreaSlot(models.Model):
    _name = 'education.kids.area.slot'
    _description = 'Kids Area Time Slot'
    _order = 'date, time_from'

    service_id = fields.Many2one('education.kids.area.service', string='Service',
                                  required=True)
    date = fields.Date(string='Date', required=True)
    time_from = fields.Float(string='From')
    time_to = fields.Float(string='To')
    capacity = fields.Integer(string='Capacity',
                               related='service_id.capacity')
    supervisor_id = fields.Many2one('education.employee', string='Supervisor')

    booked_count = fields.Integer(compute='_compute_counts',
                                    string='Booked')
    available_count = fields.Integer(compute='_compute_counts',
                                      string='Available')
    state = fields.Selection([
        ('available', 'Available'),
        ('full', 'Full'),
        ('closed', 'Closed'),
    ], string='Status', compute='_compute_state', store=True)

    booking_ids = fields.One2many('education.kids.area.booking', 'slot_id',
                                   string='Bookings')

    @api.depends('booking_ids', 'booking_ids.state', 'capacity')
    def _compute_counts(self):
        for rec in self:
            confirmed = rec.booking_ids.filtered(
                lambda b: b.state in ('confirmed', 'checked_in'))
            rec.booked_count = len(confirmed)
            rec.available_count = rec.capacity - rec.booked_count

    @api.depends('booking_ids', 'booking_ids.state', 'capacity')
    def _compute_state(self):
        for rec in self:
            confirmed = rec.booking_ids.filtered(
                lambda b: b.state in ('confirmed', 'checked_in'))
            if rec.capacity and len(confirmed) >= rec.capacity:
                rec.state = 'full'
            else:
                rec.state = 'available'


class EducationKidsAreaBooking(models.Model):
    _name = 'education.kids.area.booking'
    _description = 'Kids Area Booking'
    _inherit = ['mail.thread']
    _order = 'booking_date desc'

    slot_id = fields.Many2one('education.kids.area.slot', string='Time Slot',
                               required=True)
    student_id = fields.Many2one('res.partner', string='Student',
                                  required=True)
    parent_id = fields.Many2one('res.partner', string='Parent',
                                domain=[('is_guardian', '=', True)])
    booking_date = fields.Datetime(string='Booking Date',
                                    default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], string='Status', default='draft', tracking=True)
    amount = fields.Float(string='Amount',
                           related='slot_id.service_id.price')
    payment_status = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], string='Payment Status', default='pending')
    qr_code = fields.Char(string='QR Code', readonly=True)
    notes = fields.Text(string='Notes')

    def action_confirm(self):
        for rec in self:
            rec.qr_code = str(uuid.uuid4())
            rec.state = 'confirmed'

    def action_check_in(self):
        self.write({'state': 'checked_in'})
        for rec in self:
            self.env['education.kids.area.attendance'].create({
                'booking_id': rec.id,
                'student_id': rec.student_id.id,
                'check_in_time': fields.Datetime.now(),
                'supervisor_id': rec.slot_id.supervisor_id.id
                if rec.slot_id.supervisor_id else False,
            })

    def action_check_out(self):
        self.write({'state': 'checked_out'})
        for rec in self:
            att = self.env['education.kids.area.attendance'].search([
                ('booking_id', '=', rec.id),
                ('check_out_time', '=', False),
            ], limit=1)
            if att:
                att.check_out_time = fields.Datetime.now()

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_no_show(self):
        self.write({'state': 'no_show'})


class EducationKidsAreaAttendance(models.Model):
    _name = 'education.kids.area.attendance'
    _description = 'Kids Area Attendance'
    _order = 'check_in_time desc'

    booking_id = fields.Many2one('education.kids.area.booking',
                                  string='Booking', ondelete='cascade')
    student_id = fields.Many2one('res.partner', string='Student',
                                  required=True)
    check_in_time = fields.Datetime(string='Check In')
    check_out_time = fields.Datetime(string='Check Out')
    supervisor_id = fields.Many2one('education.employee', string='Supervisor')
    duration = fields.Float(string='Duration (Hours)',
                             compute='_compute_duration', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('check_in_time', 'check_out_time')
    def _compute_duration(self):
        for rec in self:
            if rec.check_in_time and rec.check_out_time:
                delta = rec.check_out_time - rec.check_in_time
                rec.duration = delta.total_seconds() / 3600.0
            else:
                rec.duration = 0.0


class EducationKidsAreaPackage(models.Model):
    _name = 'education.kids.area.package'
    _description = 'Kids Area Package'

    name = fields.Char(string='Package Name', required=True)
    service_ids = fields.Many2many('education.kids.area.service',
                                     string='Services')
    session_count = fields.Integer(string='Number of Sessions')
    price = fields.Float(string='Package Price')
    validity_days = fields.Integer(string='Validity (Days)', default=30)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')
