# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Default Branch
    education_default_branch_id = fields.Many2one(
        'education.branch',
        string='Default Branch',
        config_parameter='dar_elanwar.default_branch_id',
    )

    # Default Academic Year
    education_default_academic_year_id = fields.Many2one(
        'education.academic.year',
        string='Default Academic Year',
        config_parameter='dar_elanwar.default_academic_year_id',
    )

    # Student Code Settings
    education_student_code_prefix = fields.Char(
        string='Student Code Prefix',
        config_parameter='dar_elanwar.student_code_prefix',
        default='STD/',
    )

    # Employee Code Settings
    education_employee_code_prefix = fields.Char(
        string='Employee Code Prefix',
        config_parameter='dar_elanwar.employee_code_prefix',
        default='EMP/',
    )

    # Receipt Settings
    education_receipt_prefix = fields.Char(
        string='Receipt Prefix',
        config_parameter='dar_elanwar.receipt_prefix',
        default='REC/',
    )

    # Company Name for Reports
    education_company_name = fields.Char(
        string='Company Name',
        config_parameter='dar_elanwar.company_name',
    )

    # Company Logo
    education_company_logo = fields.Binary(
        string='Company Logo',
        config_parameter='dar_elanwar.company_logo',
    )

    # Enable Features
    education_enable_transportation = fields.Boolean(
        string='Enable Transportation Module',
        config_parameter='dar_elanwar.enable_transportation',
        default=True,
    )

    education_enable_inventory = fields.Boolean(
        string='Enable Inventory Module',
        config_parameter='dar_elanwar.enable_inventory',
        default=True,
    )

    education_enable_communication = fields.Boolean(
        string='Enable Communication Module',
        config_parameter='dar_elanwar.enable_communication',
        default=True,
    )
