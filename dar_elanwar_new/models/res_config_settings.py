from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_branch_id = fields.Many2one(
        'education.branch', string='Default Branch',
        default_model='education.student',
        config_parameter='dar_elanwar.default_branch_id')
    default_academic_year_id = fields.Many2one(
        'education.academic.year', string='Default Academic Year',
        default_model='education.student',
        config_parameter='dar_elanwar.default_academic_year_id')

    student_code_prefix = fields.Char(
        string='Student Code Prefix', default='STD',
        config_parameter='dar_elanwar.student_code_prefix')
    employee_code_prefix = fields.Char(
        string='Employee Code Prefix', default='EMP',
        config_parameter='dar_elanwar.employee_code_prefix')
    admission_code_prefix = fields.Char(
        string='Admission Code Prefix', default='ADM',
        config_parameter='dar_elanwar.admission_code_prefix')

    enable_kids_area = fields.Boolean(
        string='Enable Kids Area',
        config_parameter='dar_elanwar.enable_kids_area')
    enable_content_access = fields.Boolean(
        string='Enable Content Access',
        config_parameter='dar_elanwar.enable_content_access')
    enable_transportation = fields.Boolean(
        string='Enable Transportation',
        config_parameter='dar_elanwar.enable_transportation')
    enable_parent_portal = fields.Boolean(
        string='Enable Parent Portal',
        config_parameter='dar_elanwar.enable_parent_portal')

    auto_generate_invoices = fields.Boolean(
        string='Auto-Generate Invoices',
        config_parameter='dar_elanwar.auto_generate_invoices')
    auto_apply_sibling_discount = fields.Boolean(
        string='Auto-Apply Sibling Discount',
        config_parameter='dar_elanwar.auto_apply_sibling_discount')
