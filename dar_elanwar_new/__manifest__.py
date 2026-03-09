{
    'name': 'Dar Al-Anwar Academy',
    'version': '19.0.2.0.0',
    'category': 'Education',
    'summary': 'Complete Education Management System for Dar Al-Anwar Academy',
    'description': """
        Dar Al-Anwar Academy ERP Module
        ================================
        - Student & Guardian Management
        - Academic Structure (Departments, Levels, Classes, Subjects)
        - Attendance Tracking (Students & Employees)
        - Subscriptions, Billing & Discounts
        - Admission & Registration Pipeline
        - Employee HR (Salary, Loans, Penalties)
        - Kids Area Management & Booking
        - Content Access Control (Books, Games, Courses)
        - Transportation Management
        - Treasury & Inventory
        - Communication & Homework
        - 50 QWeb Reports (Arabic + English)
        - REST API with JWT Authentication
    """,
    'author': 'Dar Al-Anwar Academy',
    'website': 'https://dar-alanwar.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'web',
        'account',
        'sale',
        'purchase',
        'stock',
        'hr',
        'contacts',
    ],
    'data': [
        # Security
        'security/education_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/sequence_data.xml',
        'data/cron_data.xml',

        # Wizards
        'wizards/batch_payroll_wizard_views.xml',
        'wizards/report_wizard_views.xml',

        # Views - Configuration
        'views/menus.xml',
        'views/res_config_settings_views.xml',
        'views/education_branch_views.xml',
        'views/education_academic_year_views.xml',

        # Views - Academic
        'views/education_department_views.xml',
        'views/education_level_views.xml',
        'views/education_subject_views.xml',
        'views/education_class_views.xml',
        'views/education_schedule_views.xml',
        'views/education_grade_scale_views.xml',

        # Views - Student & Parent
        'views/education_student_views.xml',
        'views/education_parent_views.xml',

        # Views - Attendance
        'views/education_attendance_views.xml',

        # Views - Employee
        'views/education_employee_views.xml',

        # Views - Subscriptions & Billing
        'views/education_discount_views.xml',
        'views/education_subscription_views.xml',
        'views/education_payment_views.xml',

        # Views - Admission
        'views/education_admission_views.xml',

        # Views - Kids Area
        'views/education_kids_area_views.xml',

        # Views - Content Access
        'views/education_content_views.xml',

        # Views - Transportation
        'views/education_transportation_views.xml',

        # Views - Treasury & Inventory
        'views/education_treasury_views.xml',
        'views/education_inventory_views.xml',

        # Views - Communication & Homework
        'views/education_communication_views.xml',
        'views/education_homework_views.xml',

        # Views - Miscellaneous
        'views/education_daily_note_views.xml',
        'views/education_reminder_views.xml',
        'views/education_enrollment_source_views.xml',
        'views/education_leave_reason_views.xml',
        'views/education_city_views.xml',

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
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
