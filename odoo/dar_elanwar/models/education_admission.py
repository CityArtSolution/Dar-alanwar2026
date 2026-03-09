from odoo import models, fields, api, _


ADMISSION_STAGES = [
    ('application', 'Application'),
    ('assessment', 'Assessment'),
    ('accepted', 'Accepted'),
    ('enrolled', 'Enrolled'),
    ('waitlisted', 'Waitlisted'),
    ('rejected', 'Rejected'),
]


class EducationAdmissionApplication(models.Model):
    _name = 'education.admission.application'
    _description = 'Admission Application'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Application Number', readonly=True, copy=False,
                       default=lambda self: _('New'))
    student_name = fields.Char(string='Student Name (English)', required=True)
    arabic_name = fields.Char(string='Student Name (Arabic)')
    birthdate = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')

    # Guardian Info
    parent_name = fields.Char(string='Parent/Guardian Name', required=True)
    parent_phone = fields.Char(string='Parent Phone', required=True)
    parent_email = fields.Char(string='Parent Email')
    parent_national_id = fields.Char(string='Parent National ID')

    # Academic
    department_id = fields.Many2one('education.department', string='Department',
                                     required=True)
    level_id = fields.Many2one('education.level', string='Level',
                                domain="[('department_id', '=', department_id)]")
    branch_id = fields.Many2one('education.branch', string='Branch')
    academic_year_id = fields.Many2one('education.academic.year',
                                        string='Academic Year')

    # Pipeline
    stage = fields.Selection(ADMISSION_STAGES, string='Stage',
                              default='application', tracking=True)
    date = fields.Date(string='Application Date', default=fields.Date.today)
    notes = fields.Text(string='Notes')
    priority = fields.Selection([
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ], string='Priority', default='normal')
    source_id = fields.Many2one('education.enrollment.source',
                                 string='Source')

    # Documents
    document_ids = fields.One2many('education.admission.document',
                                    'application_id', string='Documents')
    document_complete = fields.Boolean(compute='_compute_document_complete',
                                        string='Documents Complete')

    # Created Student
    student_id = fields.Many2one('res.partner',
                                  string='Created Student', readonly=True,
                                  domain=[('is_student', '=', True)])

    color = fields.Integer(string='Color Index')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'education.admission.application') or _('New')
        return super().create(vals_list)

    @api.depends('document_ids.is_required', 'document_ids.is_received')
    def _compute_document_complete(self):
        for rec in self:
            required = rec.document_ids.filtered(lambda d: d.is_required)
            rec.document_complete = all(d.is_received for d in required) if required else False

    def action_assess(self):
        self.write({'stage': 'assessment'})

    def action_accept(self):
        self.write({'stage': 'accepted'})

    def action_waitlist(self):
        self.write({'stage': 'waitlisted'})

    def action_reject(self):
        self.write({'stage': 'rejected'})

    def action_enroll(self):
        """Create student record from application."""
        self.ensure_one()
        # Find or create parent
        parent = self.env['res.partner'].search([
            ('is_guardian', '=', True),
            ('id_number', '=', self.parent_national_id),
        ], limit=1)
        if not parent and self.parent_national_id:
            parent = self.env['res.partner'].create({
                'name': self.parent_name,
                'phone': self.parent_phone,
                'email': self.parent_email,
                'id_number': self.parent_national_id,
                'is_guardian': True,
                'guardian_relation': 'father',
            })

        student = self.env['res.partner'].create({
            'name': self.student_name,
            'arabic_name': self.arabic_name,
            'birthdate': self.birthdate,
            'gender': self.gender,
            'department_id': self.department_id.id,
            'branch_id': self.branch_id.id if self.branch_id else False,
            'father_id': parent.id if parent else False,
            'enrollment_date': fields.Date.today(),
            'student_state': 'enrolled',
            'enrollment_source_id': self.source_id.id if self.source_id else False,
            'is_student': True,
        })
        self.write({
            'stage': 'enrolled',
            'student_id': student.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': student.id,
            'view_mode': 'form',
        }


class EducationAdmissionCriteria(models.Model):
    _name = 'education.admission.criteria'
    _description = 'Admission Criteria'

    department_id = fields.Many2one('education.department', string='Department',
                                     required=True)
    level_id = fields.Many2one('education.level', string='Level',
                                domain="[('department_id', '=', department_id)]")
    min_age = fields.Integer(string='Minimum Age')
    max_age = fields.Integer(string='Maximum Age')
    required_documents = fields.Text(string='Required Documents')
    capacity = fields.Integer(string='Capacity')
    academic_year_id = fields.Many2one('education.academic.year',
                                        string='Academic Year')
    active = fields.Boolean(default=True)


class EducationAdmissionDocument(models.Model):
    _name = 'education.admission.document'
    _description = 'Admission Document'

    application_id = fields.Many2one('education.admission.application',
                                      string='Application', required=True,
                                      ondelete='cascade')
    name = fields.Char(string='Document Name', required=True)
    document_type = fields.Selection([
        ('birth_certificate', 'Birth Certificate'),
        ('national_id', 'National ID'),
        ('photo', 'Photo'),
        ('medical_report', 'Medical Report'),
        ('previous_school', 'Previous School Certificate'),
        ('vaccination', 'Vaccination Record'),
        ('other', 'Other'),
    ], string='Type', default='other')
    file = fields.Binary(string='File', attachment=True)
    file_name = fields.Char(string='File Name')
    is_required = fields.Boolean(string='Required', default=True)
    is_received = fields.Boolean(string='Received', default=False)
