# -*- coding: utf-8 -*-

from odoo import models, fields


class EducationSubject(models.Model):
    _name = 'education.subject'
    _description = 'Education Subject'
    _order = 'department_id, sequence, name'

    name = fields.Char(
        string='Subject Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    department_id = fields.Many2one(
        'education.department',
        string='Department',
        required=True,
        ondelete='cascade',
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    _sql_constraints = [
        ('code_department_unique', 'UNIQUE(code, department_id)',
         'Subject code must be unique within department!'),
    ]

    # Computed counts for stat buttons
    homework_count = fields.Integer(
        string='Homework',
        compute='_compute_stat_counts',
    )
    evaluation_count = fields.Integer(
        string='Evaluations',
        compute='_compute_stat_counts',
    )
    template_count = fields.Integer(
        string='Templates',
        compute='_compute_stat_counts',
    )
    student_count = fields.Integer(
        string='Students',
        compute='_compute_stat_counts',
    )

    def _compute_stat_counts(self):
        for record in self:
            record.homework_count = self.env['education.homework'].search_count([
                ('subject_id', '=', record.id)
            ])
            record.evaluation_count = self.env['education.student.evaluation'].search_count([
                ('template_id.subject_id', '=', record.id)
            ])
            record.template_count = self.env['education.evaluation.template'].search_count([
                ('subject_id', '=', record.id)
            ])
            # Students in classes of this department
            record.student_count = self.env['education.student'].search_count([
                ('department_id', '=', record.department_id.id),
                ('state', '=', 'enrolled'),
            ])

    # Stat button actions
    def action_view_homework(self):
        """View subject homework"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Homework',
            'res_model': 'education.homework',
            'view_mode': 'list,form',
            'domain': [('subject_id', '=', self.id)],
            'context': {'default_subject_id': self.id},
        }

    def action_view_evaluations(self):
        """View subject evaluations"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluations',
            'res_model': 'education.student.evaluation',
            'view_mode': 'list,form',
            'domain': [('template_id.subject_id', '=', self.id)],
        }

    def action_view_templates(self):
        """View evaluation templates for this subject"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Evaluation Templates',
            'res_model': 'education.evaluation.template',
            'view_mode': 'list,form',
            'domain': [('subject_id', '=', self.id)],
            'context': {'default_subject_id': self.id},
        }

    def action_view_students(self):
        """View students in this subject's department"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Students',
            'res_model': 'education.student',
            'view_mode': 'list,kanban,form',
            'domain': [('department_id', '=', self.department_id.id), ('state', '=', 'enrolled')],
        }

    def name_get(self):
        result = []
        for record in self:
            name = record.name
            if record.code:
                name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result
