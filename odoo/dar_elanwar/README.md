# Dar El-Anwar Educational Management System

A comprehensive Odoo 19 module for managing educational institutions that combine daycare/nursery services with Quran classes, tutoring, and other educational programs.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Module Architecture](#module-architecture)
4. [Models Overview](#models-overview)
5. [Odoo Models Integration](#odoo-models-integration)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Usage Guide](#usage-guide)
9. [Security & Permissions](#security--permissions)
10. [Reports](#reports)
11. [Technical Specifications](#technical-specifications)

---

## Overview

**Dar El-Anwar** is an educational institution management system designed to handle:

- **Daycare/Nursery** (حضانة) - Morning programs for young children
- **Quran Classes** (قرآن) - Islamic education and Quran memorization
- **Tutoring Groups** (مجموعات تقوية) - Academic support classes
- **Literacy Classes** (تعليم هجاء) - Reading and writing programs
- **Foundation Groups** (مجموعات تأسيس) - Foundation level education
- **Courses** (دورات) - Special courses (English, Arabic, Art, etc.)
- **Summer Activities** (نشاط صيفي) - Seasonal programs

### Target Users

- Educational institutions (nurseries, Islamic schools, tutoring centers)
- Administrators and management staff
- Teachers and educators
- Accountants and finance teams

---

## Features

### Student Management
- Complete student registration with personal details
- Parent/guardian information management
- Sibling tracking for marketing purposes
- Authorized pickup persons management
- Student archiving with reason tracking
- Photo management
- Multi-department enrollment (student can be in multiple programs)

### Academic Structure
- Department/Section management (Nursery, Quran, Tutoring, etc.)
- Class/Group organization
- Level/Grade management
- Subject configuration
- Schedule/Time slot management
- Academic year tracking

### Employee Management
- Teacher and staff registration
- Qualification and certification tracking
- Attendance tracking (fingerprint integration ready)
- Salary management
- Penalty and complaint tracking
- Loan/advance management

### Subscription & Payment System
- Flexible subscription types (monthly, annual, one-time)
- Automatic installment generation
- Payment tracking and receipts
- Payment reminders (configurable day)
- Unpaid subscription alerts
- Treasury/cash management

### Evaluation & Assessment
- Customizable evaluation templates
- Multiple grading scales (Yes/No, Excellent/Good/Acceptable, etc.)
- Individual and shared goals
- Evaluation history per student
- PDF report generation
- Email evaluation reports to parents

### Attendance Tracking
- Daily student attendance
- Department and class-based recording
- Absence alerts (configurable days)
- Attendance reports and Excel export
- Print blank sheets for manual tracking

### Transportation
- Bus and driver management
- Route configuration
- Student transport assignment
- Pickup method tracking (self, parent, bus)

### Inventory Management
- Book and product catalog
- Stock incoming (purchases)
- Stock outgoing (sales)
- Automatic stock balance calculation
- Integration with treasury

### Communication
- Email templates for common messages
- Evaluation reports to parents
- Payment reminders
- Absence notifications
- Sibling enrollment age alerts

### Dashboard & Reports
- Real-time student count
- Daily absence count
- Treasury balance
- Income/Expense charts
- Student age reports
- Parent information reports
- Subscription status reports

---

## Module Architecture

```
dar_elanwar/
├── __init__.py
├── __manifest__.py
├── README.md
├── security/
│   ├── ir.model.access.csv
│   └── education_security.xml
├── models/
│   ├── __init__.py
│   ├── res_partner.py              # Students, Parents, Drivers
│   ├── hr_employee.py              # Teachers/Staff extensions
│   ├── education_academic.py       # Department, Class, Level, Subject
│   ├── education_enrollment.py     # Student enrollment
│   ├── education_subscription.py   # Subscriptions & Payments
│   ├── education_evaluation.py     # Evaluations & Assessments
│   ├── education_attendance.py     # Student attendance
│   ├── education_employee.py       # Salary, Penalties, Loans
│   ├── education_transport.py      # Buses & Routes
│   ├── education_homework.py       # Homework tracking
│   └── education_config.py         # Settings & Configuration
├── views/
│   ├── student_views.xml
│   ├── parent_views.xml
│   ├── employee_views.xml
│   ├── academic_views.xml
│   ├── subscription_views.xml
│   ├── evaluation_views.xml
│   ├── attendance_views.xml
│   ├── transport_views.xml
│   ├── treasury_views.xml
│   ├── inventory_views.xml
│   ├── config_views.xml
│   └── menu_views.xml
├── reports/
│   ├── student_report.xml
│   ├── payment_receipt_report.xml
│   ├── evaluation_report.xml
│   └── attendance_report.xml
├── data/
│   ├── sequences.xml
│   ├── default_data.xml
│   └── mail_templates.xml
├── wizard/
│   ├── bulk_attendance_wizard.xml
│   └── bulk_payment_wizard.xml
└── static/
    └── description/
        ├── icon.png
        └── banner.png
```

---

## Models Overview

### Summary Table

| Category | Total Models | Inherit Existing | Create New |
|----------|-------------|------------------|------------|
| Student Management | 6 | 2 | 4 |
| Academic Structure | 7 | 1 | 6 |
| Employee Management | 8 | 5 | 3 |
| Subscriptions & Payments | 6 | 3 | 3 |
| Evaluation & Assessment | 7 | 5 | 2 |
| Attendance | 2 | 1 | 1 |
| Transportation | 4 | 4 | 0 |
| Treasury & Accounting | 5 | 3 | 2 |
| Inventory | 5 | 4 | 1 |
| Communication | 3 | 3 | 0 |
| Configuration | 6 | 2 | 4 |
| System & Users | 4 | 2 | 2 |
| Homework | 2 | 0 | 2 |
| **TOTAL** | **65** | **35** | **30** |

### Detailed Model List

#### 1. Student Management Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `res.partner` (extended) | الطالب | Inherit | Student records with `is_student=True` |
| `res.partner` (extended) | ولي الأمر | Inherit | Parent records with `is_parent=True` |
| `education.authorized.pickup` | المصرح لهم | New | Authorized pickup persons |
| `education.sibling` | الإخوة | New | Sibling information for marketing |
| `education.student.note` | ملاحظات | New | Student observations/notes |
| `education.student.archive` | الأرشيف | New | Archive history with reasons |

#### 2. Academic Structure Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `education.department` | القسم | New | Nursery, Quran, Tutoring, etc. |
| `education.level` | المستوى | New | Grade levels (1st, 2nd, 3rd...) |
| `education.class` | الفصل | New | Classes/Groups |
| `education.subject` | المادة | New | Subjects (Arabic, English, Math) |
| `education.schedule` | الميعاد | New | Time slots |
| `education.academic.year` | العام الدراسي | New | Academic years |
| `education.student.enrollment` | التسجيل | New | Student-Department enrollment |

#### 3. Employee Management Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `hr.employee` (extended) | الموظف | Inherit | Teachers and staff |
| `hr.employee.category` | التصنيف | Use Existing | Admin, Teaching, etc. |
| `hr.attendance` | الحضور | Use Existing | Employee attendance |
| `education.employee.qualification` | المؤهلات | New | Qualifications/Certificates |
| `education.employee.salary` | الرواتب | New | Monthly salary records |
| `education.employee.penalty` | الجزاءات | New | Disciplinary actions |
| `education.employee.complaint` | الشكاوى | New | Complaints |
| `education.employee.loan` | السلف | New | Salary advances |

#### 4. Subscription & Payment Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `product.product` (extended) | نوع الاشتراك | Inherit | Subscription types as products |
| `education.payment.plan` | نظام السداد | New | Monthly, Annual, One-time |
| `education.student.subscription` | اشتراك الطالب | New | Student subscriptions |
| `education.installment` | الدفعات | New | Individual installments |
| `account.payment` (extended) | السداد | Inherit | Payment transactions |
| `account.move` | الإيصال | Use Existing | Payment receipts |

#### 5. Evaluation & Assessment Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `education.grade.scale` | مقياس التقييم | New | Grading scales |
| `education.grade.scale.value` | قيم المقياس | New | Scale values |
| `survey.survey` (extended) | قالب التقييم | Inherit | Evaluation templates |
| `survey.question` | الأسئلة | Use Existing | Evaluation questions |
| `education.evaluation.goal` | الأهداف | New | Evaluation goals |
| `survey.user_input` (extended) | تقييم الطالب | Inherit | Student evaluations |
| `survey.user_input.line` | الإجابات | Use Existing | Evaluation answers |

#### 6. Attendance Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `education.attendance` | الحضور | New | Daily attendance session |
| `education.attendance.line` | سطر الحضور | New | Individual student attendance |

#### 7. Transportation Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `fleet.vehicle` (extended) | الباص | Inherit | Buses |
| `res.partner` (extended) | السائق | Inherit | Drivers with `is_driver=True` |
| `education.bus.route` | خط السير | New | Bus routes |
| (fields on res.partner) | مواصلات الطالب | Inherit | Transport assignment |

#### 8. Treasury & Accounting Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `account.journal` | الخزينة | Use Existing | Cash journal |
| `account.move` | الحركات | Use Existing | Transactions |
| `account.account` | الحسابات | Use Existing | Chart of accounts |
| `education.income.type` | أنواع الإيراد | New | Income categories |
| `education.expense.type` | أنواع المصروف | New | Expense categories |

#### 9. Inventory Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `product.category` | تصنيف المنتج | Use Existing | Book categories |
| `product.product` | الكتب | Use Existing | Books/Products |
| `stock.picking` | حركة المخزون | Use Existing | Stock in/out |
| `stock.move` | سطر الحركة | Use Existing | Stock lines |

#### 10. Communication Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `mail.template` | قوالب الرسائل | Use Existing | Message templates |
| `mail.mail` | الرسائل | Use Existing | Emails |
| `mail.message` | سجل الرسائل | Use Existing | Message log |

#### 11. Configuration Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `res.company` | الفرع | Use Existing | Branches (multi-company) |
| `education.enrollment.source` | مصدر التعرف | New | How they heard about us |
| `education.leave.reason` | سبب الانقطاع | New | Reasons for leaving |
| `res.config.settings` (extended) | الإعدادات | Inherit | System settings |

#### 12. System Models

| Model | Arabic Name | Type | Description |
|-------|-------------|------|-------------|
| `res.groups` | الصلاحيات | Use Existing | User permissions |
| `calendar.event` | التذكيرات | Use Existing | Reminders |
| `education.daily.note` | ملاحظات يومية | New | Dashboard notes |
| `education.homework` | الواجبات | New | Homework assignments |
| `education.student.homework` | واجب الطالب | New | Student homework status |

---

## Odoo Models Integration

### Models We Inherit (Extend)

#### res.partner (Students, Parents, Drivers)
```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Student fields
    is_student = fields.Boolean()
    student_code = fields.Char()
    enrollment_date = fields.Date()
    period = fields.Selection([('morning', 'Morning'), ('evening', 'Evening')])
    department_id = fields.Many2one('education.department')
    class_id = fields.Many2one('education.class')

    # Parent fields
    is_parent = fields.Boolean()
    marital_status = fields.Selection()

    # Driver fields
    is_driver = fields.Boolean()
    license_number = fields.Char()

    # Transport fields (for students)
    bus_id = fields.Many2one('fleet.vehicle')
    driver_id = fields.Many2one('res.partner', domain=[('is_driver','=',True)])
    pickup_method = fields.Selection()
```

#### hr.employee (Teachers/Staff)
```python
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    teacher_code = fields.Char()
    is_teacher = fields.Boolean()
    qualification = fields.Char()
    university = fields.Char()
    graduation_date = fields.Date()
```

#### product.product (Subscription Types)
```python
class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_subscription = fields.Boolean()
    department_id = fields.Many2one('education.department')
    payment_plan_id = fields.Many2one('education.payment.plan')
```

#### survey.survey (Evaluation Templates)
```python
class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    subject_id = fields.Many2one('education.subject')
    department_id = fields.Many2one('education.department')
```

#### fleet.vehicle (Buses)
```python
class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    is_school_bus = fields.Boolean()
    route_id = fields.Many2one('education.bus.route')
    student_ids = fields.One2many('res.partner', 'bus_id')
```

---

## Installation

### Prerequisites

- Odoo 19 Community or Enterprise
- Python 3.10+
- PostgreSQL 14+

### Required Odoo Modules

```python
'depends': [
    'base',           # Core
    'contacts',       # Contact management
    'hr',             # Human Resources
    'hr_attendance',  # Employee attendance
    'product',        # Products
    'stock',          # Inventory
    'account',        # Accounting
    'fleet',          # Vehicle management
    'survey',         # Surveys/Evaluations
    'mail',           # Messaging
    'calendar',       # Calendar/Reminders
],
```

### Installation Steps

1. **Clone/Copy the module:**
   ```bash
   cd /path/to/odoo/custom/addons
   git clone <repository_url> dar_elanwar
   # OR copy the folder manually
   ```

2. **Update Odoo configuration:**
   ```conf
   # odoo.conf
   addons_path = /path/to/odoo/addons,/path/to/odoo/custom/addons
   ```

3. **Restart Odoo:**
   ```bash
   sudo systemctl restart odoo
   # OR
   ./odoo-bin -c odoo.conf
   ```

4. **Install the module:**
   - Go to Apps menu
   - Remove "Apps" filter
   - Search for "Dar El-Anwar"
   - Click Install

5. **Install required modules:**
   The system will automatically install dependencies.

---

## Configuration

### Initial Setup

1. **System Settings** (Settings > Education Settings)
   - Institution name and logo
   - Receipt paper size (A4/A5)
   - Payment reminder day (default: 10)
   - Absence alert threshold (default: 3 days)
   - Sibling notification age (default: 3.5 years)
   - Email configuration

2. **Academic Structure**
   - Create Departments (Nursery, Quran, Tutoring, etc.)
   - Create Levels/Grades
   - Create Classes
   - Create Subjects
   - Create Schedules/Time slots

3. **Subscription Types**
   - Create products for each subscription type
   - Set prices and payment plans
   - Link to departments

4. **Evaluation Templates**
   - Create grade scales (Yes/No, Excellent/Good/Acceptable)
   - Create evaluation templates with questions
   - Link to subjects

5. **Transportation**
   - Add buses (fleet vehicles)
   - Add drivers
   - Configure routes

6. **User Permissions**
   - Create user groups (Admin, Teacher, Secretary, Accountant)
   - Assign permissions

---

## Usage Guide

### Registering a New Student

1. Go to **Students > Add Student**
2. Fill in personal information:
   - Name, birthdate, photo
   - City, address
   - Period (morning/evening)
3. Select department and class
4. Add parent information:
   - Father details (name, job, phone)
   - Mother details (name, job, phone)
5. Configure:
   - Enrollment source (how they heard about us)
   - Transport method
   - Authorized pickup persons
   - Sibling information
6. Save and print application form

### Creating Subscriptions

1. Go to **Students > [Student Name] > Subscriptions**
2. Click "Add Subscription"
3. Select:
   - Subscription type (Nursery Fees, Quran Fees, etc.)
   - Payment plan (Monthly, Annual)
4. System auto-generates installments
5. Save

### Recording Payments

1. Go to **Students > [Student Name] > Subscriptions**
2. Click "Pay" on the installment
3. Select payment method
4. Print receipt

### Recording Attendance

1. Go to **Attendance > Daily Attendance**
2. Select date, department, class
3. All students show as "Present" by default
4. Mark absent students
5. Save

### Creating Evaluations

1. Go to **Evaluations > Goals**
2. Create goal:
   - Select teacher, subject, class
   - Select evaluation template
   - Set shared or individual goal
3. Go to **Evaluations > Student Evaluations**
4. Select student and answer questions
5. Add summary notes
6. Save and send to parent via email

---

## Security & Permissions

### User Groups

| Group | Access Level |
|-------|--------------|
| Education / Admin | Full access to all features |
| Education / Manager | All except settings and user management |
| Education / Teacher | Evaluations, attendance, homework |
| Education / Secretary | Students, subscriptions, payments |
| Education / Accountant | Treasury, payments, reports |
| Education / User | Read-only access |

### Record Rules

- Teachers can only see their own classes
- Secretaries cannot see salary information
- Accountants cannot delete treasury entries
- Parents (portal) can only see their children

---

## Reports

### Available Reports

1. **Student Reports**
   - Student list by department/class
   - Students by age range
   - Birthday list
   - Parent contact list
   - Sibling report

2. **Financial Reports**
   - Daily treasury report
   - Income analysis (with charts)
   - Expense analysis
   - Subscription status (paid/unpaid)
   - Payment receipts

3. **Attendance Reports**
   - Daily attendance by class
   - Monthly attendance summary
   - Absence report

4. **Evaluation Reports**
   - Student evaluation (PDF for parents)
   - Class evaluation summary
   - Teacher evaluation statistics

5. **Inventory Reports**
   - Stock balance
   - Stock movements

---

## Technical Specifications

### Database Requirements

- PostgreSQL 14+
- Recommended: 4GB RAM minimum
- Storage: Depends on student count and attachments

### Performance Considerations

- Indexed fields: student_code, date fields, foreign keys
- Computed fields are stored where appropriate
- Batch operations for bulk attendance and payments

### API Endpoints

The module uses standard Odoo ORM and can be accessed via:
- XML-RPC
- JSON-RPC
- REST API (if web_api module installed)

### Backup Recommendations

- Daily database backup
- Attachment folder backup
- Configuration file backup

---

## Support

For issues and feature requests, please contact:
- GitHub Issues: [repository_url]/issues
- Email: support@example.com

---

## License

This module is licensed under LGPL-3.

---

## Changelog

### Version 1.0.0 (Initial Release)
- Complete student management
- Academic structure
- Subscription and payment system
- Evaluation system
- Attendance tracking
- Transportation management
- Treasury and accounting integration
- Inventory management
- Communication system
- Dashboard and reports

---

## Credits

- **Author:** [Your Name/Company]
- **Contributors:** [List of contributors]
- **Based on requirements from:** Dar El-Anwar Educational Institution

---

*Document Version: 1.0*
*Last Updated: December 2024*
*Odoo Version: 19.0*
