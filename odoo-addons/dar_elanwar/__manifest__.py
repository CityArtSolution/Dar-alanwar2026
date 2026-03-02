# -*- coding: utf-8 -*-
{
    'name': 'Dar El-Anwar Educational Management',
    'version': '19.0.2.0.0',
    'category': 'Education',
    'summary': 'Complete Educational Institution Management System',
    'description': """
Dar El-Anwar Educational Management System
===========================================

A comprehensive educational institution management system for managing:
- Students and Parents (Enhanced profiles)
- Employees and Teachers (Batch payroll, shift types)
- Academic Structure (Departments, Classes, Levels)
- Subscriptions, Payments & Discounts
- Attendance Tracking (with time tracking)
- Evaluations and Assessments
- Admission & Registration Pipeline
- Kids Area Management & Booking
- Content Access Control (Books, Games, Courses)
- Transportation (Buses and Drivers)
- Treasury and Transactions
- Inventory (Books and Products)
- Communication and Messaging
- Homework and Activities
- 10 QWeb Reports (Arabic + English)
- REST API with JWT Authentication
    """,
    'author': 'Dar Al-Anwar Academy',
    'website': 'https://dar-alanwar.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'web'],
    'data': [
        # Security
        'security/education_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/education_sequence.xml',
        'data/cron_data.xml',

        # Wizards
        'wizards/batch_payroll_wizard_views.xml',
        'wizards/report_wizard_views.xml',

        # Views - Original
        'views/config_views.xml',
        'views/academic_views.xml',
        'views/student_views.xml',
        'views/employee_views.xml',
        'views/subscription_views.xml',
        'views/attendance_views.xml',
        'views/evaluation_views.xml',
        'views/transport_views.xml',
        'views/treasury_views.xml',
        'views/inventory_views.xml',
        'views/communication_views.xml',
        'views/homework_views.xml',
        'views/menu_views.xml',

        # Views - New Modules
        'views/education_discount_views.xml',
        'views/education_admission_views.xml',
        'views/education_kids_area_views.xml',
        'views/education_content_views.xml',
        'views/res_config_settings_views.xml',

        # Reports
        'reports/report_paperformat.xml',
        'reports/report_actions.xml',
        'reports/templates/report_student_details.xml',
        'reports/templates/report_student_statistics.xml',
        'reports/templates/report_attendance.xml',
        'reports/templates/report_financial.xml',
        'reports/templates/report_employee.xml',
        'reports/templates/report_goals.xml',
        'reports/templates/report_kids_area.xml',
        'reports/templates/report_inventory.xml',
        'reports/templates/report_communication.xml',
        'reports/templates/report_course.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dar_elanwar/static/src/css/education.css',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}
