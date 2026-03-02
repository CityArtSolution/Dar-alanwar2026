# -*- coding: utf-8 -*-

from odoo import models, fields, api

HOMEWORK_STATES = [
    ('draft', 'Draft'),
    ('assigned', 'Assigned'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class EducationHomework(models.Model):
    _name = 'education.homework'
    _description = 'Homework'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'due_date desc, id desc'

    name = fields.Char(
        string='Title',
        required=True,
        tracking=True,
    )
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        required=True,
    )
    subject_id = fields.Many2one(
        'education.subject',
        string='Subject',
        required=True,
    )
    teacher_id = fields.Many2one(
        'education.employee',
        string='Teacher',
        required=True,
        domain="[('is_teacher', '=', True)]",
    )
    date = fields.Date(
        string='Assigned Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    due_date = fields.Date(
        string='Due Date',
        required=True,
        tracking=True,
    )
    description = fields.Html(
        string='Description',
    )
    attachment = fields.Binary(
        string='Attachment',
        attachment=True,
    )
    attachment_name = fields.Char(
        string='Attachment Name',
    )
    state = fields.Selection(
        selection=HOMEWORK_STATES,
        string='Status',
        default='draft',
        tracking=True,
    )
    notes = fields.Text(
        string='Notes',
    )

    # Related
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        related='class_id.department_id',
        store=True,
    )

    # Student submissions
    submission_ids = fields.One2many(
        'education.student.homework',
        'homework_id',
        string='Submissions',
    )

    # Computed
    submission_count = fields.Integer(
        string='Submission Count',
        compute='_compute_submission_count',
    )
    completed_count = fields.Integer(
        string='Completed Count',
        compute='_compute_submission_count',
    )

    @api.depends('submission_ids', 'submission_ids.status')
    def _compute_submission_count(self):
        for record in self:
            record.submission_count = len(record.submission_ids)
            record.completed_count = len(record.submission_ids.filtered(lambda s: s.status == 'completed'))

    # Stat button actions
    def action_view_submissions(self):
        """View homework submissions"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Submissions',
            'res_model': 'education.student.homework',
            'view_mode': 'list,form',
            'domain': [('homework_id', '=', self.id)],
            'context': {'default_homework_id': self.id},
        }

    def action_view_class(self):
        """View homework class"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Class',
            'res_model': 'education.class',
            'view_mode': 'form',
            'res_id': self.class_id.id,
        }

    def action_view_teacher(self):
        """View homework teacher"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Teacher',
            'res_model': 'education.employee',
            'view_mode': 'form',
            'res_id': self.teacher_id.id,
        }

    def action_assign(self):
        """Assign homework to all students in the class"""
        for record in self:
            students = self.env['education.student'].search([
                ('class_id', '=', record.class_id.id),
                ('state', '=', 'enrolled'),
            ])
            for student in students:
                existing = self.env['education.student.homework'].search([
                    ('homework_id', '=', record.id),
                    ('student_id', '=', student.id),
                ], limit=1)
                if not existing:
                    self.env['education.student.homework'].create({
                        'homework_id': record.id,
                        'student_id': student.id,
                        'status': 'pending',
                    })
            record.state = 'assigned'

    def action_complete(self):
        """Mark homework as completed"""
        self.write({'state': 'completed'})

    def action_cancel(self):
        """Cancel the homework"""
        self.write({'state': 'cancelled'})

    def action_reset(self):
        """Reset to draft"""
        self.write({'state': 'draft'})


class EducationStudentHomework(models.Model):
    _name = 'education.student.homework'
    _description = 'Student Homework Submission'
    _order = 'homework_id, student_id'

    SUBMISSION_STATUS = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
        ('late', 'Late'),
        ('not_done', 'Not Done'),
    ]

    homework_id = fields.Many2one(
        'education.homework',
        string='Homework',
        required=True,
        ondelete='cascade',
    )
    student_id = fields.Many2one(
        'education.student',
        string='Student',
        required=True,
    )
    status = fields.Selection(
        selection=SUBMISSION_STATUS,
        string='Status',
        default='pending',
        required=True,
    )
    submission_date = fields.Date(
        string='Submission Date',
    )
    notes = fields.Text(
        string='Notes',
    )
    attachment = fields.Binary(
        string='Attachment',
        attachment=True,
    )
    attachment_name = fields.Char(
        string='Attachment Name',
    )
    grade = fields.Char(
        string='Grade',
    )
    teacher_notes = fields.Text(
        string='Teacher Notes',
    )

    # Related
    class_id = fields.Many2one(
        'education.class',
        string='Class',
        related='homework_id.class_id',
        store=True,
    )
    due_date = fields.Date(
        string='Due Date',
        related='homework_id.due_date',
        store=True,
    )

    _sql_constraints = [
        ('homework_student_unique', 'UNIQUE(homework_id, student_id)',
         'Each student can only have one submission per homework!'),
    ]

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.homework_id.name} - {record.student_id.name}"
            result.append((record.id, name))
        return result
