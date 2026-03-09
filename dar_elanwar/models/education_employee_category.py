# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationEmployeeCategory(models.Model):
    _name = 'education.employee.category'
    _description = 'Employee Category'
    _order = 'sequence, name'

    name = fields.Char(
        string='Category Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    description = fields.Text(
        string='Description',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # Related records
    employee_ids = fields.One2many(
        'education.employee',
        'category_id',
        string='Employees',
    )

    # Computed counts
    employee_count = fields.Integer(
        string='Employee Count',
        compute='_compute_employee_count',
    )

    @api.depends('employee_ids')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = len(record.employee_ids)

    def action_view_employees(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employees',
            'res_model': 'education.employee',
            'view_mode': 'list,form',
            'domain': [('category_id', '=', self.id)],
            'context': {'default_category_id': self.id},
        }

    _name_unique = models.Constraint(
        'UNIQUE(name)',
        'Category name must be unique!',
    )
