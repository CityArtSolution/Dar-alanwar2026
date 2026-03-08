from odoo import models, fields, api


class EducationContentCategory(models.Model):
    _name = 'education.content.category'
    _description = 'Content Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Code')
    content_type = fields.Selection([
        ('book', 'Book'),
        ('game', 'Interactive Game'),
        ('course', 'Video Course'),
        ('video', 'Video'),
        ('kids_area', 'Kids Area Activity'),
    ], string='Content Type', required=True)
    icon = fields.Char(string='Icon Class')
    active = fields.Boolean(default=True)
    item_count = fields.Integer(compute='_compute_item_count', string='Items')

    def _compute_item_count(self):
        for rec in self:
            rec.item_count = self.env['education.content.item'].search_count(
                [('category_id', '=', rec.id)])


class EducationContentItem(models.Model):
    _name = 'education.content.item'
    _description = 'Content Item'
    _inherit = ['mail.thread']

    name = fields.Char(string='Title', required=True, tracking=True)
    category_id = fields.Many2one('education.content.category',
                                    string='Category', required=True)
    content_type = fields.Selection(related='category_id.content_type',
                                      store=True, string='Type')
    description = fields.Text(string='Description')
    file_url = fields.Char(string='File URL')
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    thumbnail = fields.Binary(string='Thumbnail', attachment=True)

    grade_level_ids = fields.Many2many('education.level',
                                         'content_item_level_rel',
                                         'item_id', 'level_id',
                                         string='Grade Levels')
    target_age_min = fields.Integer(string='Min Target Age')
    target_age_max = fields.Integer(string='Max Target Age')
    is_drm_protected = fields.Boolean(string='DRM Protected', default=False)
    active = fields.Boolean(default=True)

    access_count = fields.Integer(compute='_compute_access_count',
                                    string='Access Granted')

    def _compute_access_count(self):
        for rec in self:
            rec.access_count = self.env['education.content.access'].search_count(
                [('content_item_id', '=', rec.id), ('is_active', '=', True)])


class EducationContentAccess(models.Model):
    _name = 'education.content.access'
    _description = 'Content Access Grant'
    _order = 'granted_date desc'

    student_id = fields.Many2one('res.partner', string='Student',
                                  required=True)
    content_item_id = fields.Many2one('education.content.item',
                                       string='Content Item', required=True)
    granted_by = fields.Many2one('res.users', string='Granted By',
                                  default=lambda self: self.env.user)
    granted_date = fields.Date(string='Grant Date', default=fields.Date.today)
    revoked_date = fields.Date(string='Revoked Date')
    is_active = fields.Boolean(string='Active', default=True)
    expiry_date = fields.Date(string='Expiry Date')

    def action_revoke(self):
        self.write({
            'is_active': False,
            'revoked_date': fields.Date.today(),
        })


class EducationContentUsage(models.Model):
    _name = 'education.content.usage'
    _description = 'Content Usage Log'
    _order = 'access_date desc'

    student_id = fields.Many2one('res.partner', string='Student',
                                  required=True)
    content_item_id = fields.Many2one('education.content.item',
                                       string='Content Item', required=True)
    access_date = fields.Datetime(string='Access Date',
                                    default=fields.Datetime.now)
    duration_minutes = fields.Integer(string='Duration (Minutes)')
    completed = fields.Boolean(string='Completed', default=False)
    score = fields.Float(string='Score')
