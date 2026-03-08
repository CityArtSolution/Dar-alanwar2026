from odoo import models, fields, api


class ReportWizard(models.TransientModel):
    _name = 'education.report.wizard'
    _description = 'Report Filter Wizard'

    report_type = fields.Selection([
        ('student_details', 'Student Details'),
        ('student_statistics', 'Student Statistics'),
        ('attendance', 'Attendance Report'),
        ('financial', 'Financial Report'),
        ('employee', 'Employee Report'),
        ('goals', 'Goals Report'),
        ('kids_area', 'Kids Area Report'),
        ('inventory', 'Inventory Report'),
    ], string='Report Type', required=True)

    date_from = fields.Date(string='From Date')
    date_to = fields.Date(string='To Date')
    branch_id = fields.Many2one('education.branch', string='Branch')
    department_id = fields.Many2one('education.department', string='Department')
    class_id = fields.Many2one('education.class', string='Class',
                                domain="[('department_id', '=', department_id)]")
    academic_year_id = fields.Many2one('education.academic.year',
                                        string='Academic Year')
    student_id = fields.Many2one('res.partner', string='Student',
                                    domain=[('is_student', '=', True)])
    employee_id = fields.Many2one('education.employee', string='Employee')

    def action_print_report(self):
        self.ensure_one()
        report_map = {
            'student_details': 'dar_elanwar.action_report_student_details',
            'student_statistics': 'dar_elanwar.action_report_student_statistics',
            'attendance': 'dar_elanwar.action_report_attendance',
            'financial': 'dar_elanwar.action_report_financial',
            'employee': 'dar_elanwar.action_report_employee',
            'goals': 'dar_elanwar.action_report_goals',
            'kids_area': 'dar_elanwar.action_report_kids_area',
            'inventory': 'dar_elanwar.action_report_inventory',
        }

        data = {
            'date_from': str(self.date_from) if self.date_from else False,
            'date_to': str(self.date_to) if self.date_to else False,
            'branch_id': self.branch_id.id if self.branch_id else False,
            'department_id': self.department_id.id if self.department_id else False,
            'class_id': self.class_id.id if self.class_id else False,
            'academic_year_id': self.academic_year_id.id if self.academic_year_id else False,
            'student_id': self.student_id.id if self.student_id else False,
            'employee_id': self.employee_id.id if self.employee_id else False,
        }

        report_action = report_map.get(self.report_type)
        if report_action:
            return self.env.ref(report_action).report_action(self, data=data)
