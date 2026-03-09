from odoo import models, fields, api


class EducationClass(models.Model):
    _name = 'education.class'
    _description = 'Education Class'
    _inherit = ['mail.thread']

    name = fields.Char(string='Class Name', required=True, tracking=True)
    code = fields.Char(string='Code', required=True)
    department_id = fields.Many2one('education.department', string='Department',
                                     required=True)
    level_id = fields.Many2one('education.level', string='Level',
                                domain="[('department_id', '=', department_id)]")
    schedule_id = fields.Many2one('education.schedule', string='Schedule')
    capacity = fields.Integer(string='Capacity', default=30)
    teacher_id = fields.Many2one('education.employee', string='Teacher',
                                  domain=[('is_teacher', '=', True)])
    room = fields.Char(string='Room')
    active = fields.Boolean(default=True)

    student_ids = fields.One2many('education.student', 'class_id', string='Students')
    student_count = fields.Integer(compute='_compute_student_count', string='Enrolled')
    available_seats = fields.Integer(compute='_compute_student_count', string='Available')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Class code must be unique!'),
    ]

    @api.depends('student_ids', 'capacity')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids.filtered(
                lambda s: s.state == 'enrolled'))
            rec.available_seats = rec.capacity - rec.student_count
