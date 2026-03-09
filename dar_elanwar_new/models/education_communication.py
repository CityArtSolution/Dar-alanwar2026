from odoo import models, fields, api, _


class EducationAnnouncement(models.Model):
    _name = 'education.announcement'
    _description = 'Announcement'
    _inherit = ['mail.thread']
    _order = 'date desc'

    title = fields.Char(string='Title', required=True, tracking=True)
    content = fields.Html(string='Content')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    author_id = fields.Many2one('res.users', string='Author',
                                 default=lambda self: self.env.user)
    target_type = fields.Selection([
        ('all', 'All'),
        ('department', 'Department'),
        ('class', 'Class'),
        ('parents', 'Parents Only'),
        ('employees', 'Employees Only'),
    ], string='Target', default='all')
    department_id = fields.Many2one('education.department', string='Department')
    class_id = fields.Many2one('education.class', string='Class')
    branch_id = fields.Many2one('education.branch', string='Branch')
    is_published = fields.Boolean(string='Published', default=False)
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal')


class EducationMessage(models.Model):
    _name = 'education.message'
    _description = 'Internal Message'
    _order = 'date desc'

    subject = fields.Char(string='Subject', required=True)
    body = fields.Html(string='Message Body')
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    sender_id = fields.Many2one('res.users', string='Sender',
                                 default=lambda self: self.env.user)
    recipient_type = fields.Selection([
        ('parent', 'Parent'),
        ('employee', 'Employee'),
        ('user', 'System User'),
    ], string='Recipient Type')
    parent_id = fields.Many2one('education.parent', string='Parent')
    employee_id = fields.Many2one('education.employee', string='Employee')
    user_id = fields.Many2one('res.users', string='User')
    is_read = fields.Boolean(string='Read', default=False)
    read_date = fields.Datetime(string='Read Date')

    def action_mark_read(self):
        self.write({
            'is_read': True,
            'read_date': fields.Datetime.now(),
        })


class EducationSupportTicket(models.Model):
    _name = 'education.support.ticket'
    _description = 'Support Ticket'
    _inherit = ['mail.thread']
    _order = 'create_date desc'

    name = fields.Char(string='Ticket Number', readonly=True,
                       default=lambda self: _('New'))
    subject = fields.Char(string='Subject', required=True, tracking=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('education.parent', string='Parent')
    student_id = fields.Many2one('education.student', string='Student')
    category = fields.Selection([
        ('academic', 'Academic'),
        ('financial', 'Financial'),
        ('technical', 'Technical'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('other', 'Other'),
    ], string='Category', default='other')
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='new', tracking=True)
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    resolution = fields.Text(string='Resolution')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'education.support.ticket') or _('New')
        return super().create(vals_list)
