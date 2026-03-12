# Dar Al-Anwar Academy Management System — PRD v4.0 + Task Tracker v2.0 Status

> **Project:** Dar Al-Anwar Academy Management System
> **Developer:** Moaaz Nabil
> **Version:** PRD v4.0 + Task Tracker v2.0 | Status Date: March 12, 2026
> **Total Budget:** $2,000 USD (Fixed Price)
> **Timeline:** 50 Calendar Days | 5 Phases | 29 Tasks
> **Scope:** Odoo 19 Backend + Vue.js Portal (Parent/Student/Teacher/Admin) + REST API + 50 Reports + Paymob

---

## 1. Project Overview

Dar Al-Anwar is an educational academy (nursery, courses, online) with TWO integrated systems:

| System | Technology | Purpose |
|--------|-----------|---------|
| Odoo 19 Backend | Odoo Community (Python) | Full ERP: students, billing, HR, inventory, reports |
| Web Portal | Vue.js 3 + Vite + Tailwind | Website for Parent, Student, Teacher, Admin |
| REST API Layer | Odoo Controllers + JWT | Bidirectional sync: Portal <-> Odoo |

**KEY PRINCIPLE:** Odoo is the backend for EVERYTHING. The Portal reads/writes to Odoo via API.

### 1.1 Portal User Types

| User Type | Login | Main Features |
|-----------|-------|---------------|
| Parent | Separate login | View children, buy content, pay via Paymob, invoices, book Kids Area |
| Student | Separate login | Games, books, attendance, homework, grades, goals, chat |
| Teacher | Separate login | Attendance, assignments, assessments, goals, communication |
| Admin | Separate login | Full control: users, content, billing, bookings, reports |

### 1.2 Portal Account Creation

| User Type | Who Creates | Notes |
|-----------|------------|-------|
| Parent | Self-signup OR Admin | Parent registers, admin approves; OR admin creates directly |
| Student | Parent creates OR Admin | Only those who need portal get an account |
| Teacher | Admin creates | Admin creates from dashboard |
| Admin | Super Admin creates | Only super admin can create other admins |

---

## 2. System Architecture

### 2.1 Data Flow (Bidirectional Sync)

| Action | Direction | Example |
|--------|-----------|---------|
| Admin adds student in Odoo | Odoo -> Portal | Student appears in portal |
| Parent buys content | Portal -> Odoo | Invoice created, content access granted |
| Teacher marks attendance | Portal -> Odoo | Saved in Odoo, parent/student sees it |
| Admin assigns content | Odoo -> Portal | Student sees new content |
| Parent pays via Paymob | Portal -> Paymob -> Odoo | Payment recorded, invoice marked paid |
| Student completes assignment | Portal -> Odoo | Submission saved, teacher sees it |

### 2.2 User Roles

| Role | System Access | Capabilities |
|------|-------------|-------------|
| Super Admin | Odoo + Portal | Full control of everything |
| Branch Admin | Odoo + Portal | Manage their branch only |
| Teacher | Portal ONLY | Attendance, assignments, assessments |
| Parent | Portal ONLY | View children, buy content, pay, book |
| Student | Portal ONLY | Games, books, attendance, homework, grades |

---

## 3. Task Tracker v2.0 — Official Task Status

> Source: `DarAlAnwar_Task_Tracker_v2.docx` (March 12, 2026)
> 29 Tasks | 5 Phases | 50 Days | 6 NEW features added in v2.0

### Phase Summary

| Phase | Days | Payment | Tracker Status | Actual Status |
|-------|------|---------|---------------|---------------|
| Phase 1 — Foundation & Setup | Days 1-10 | $600 | In Progress | **Nearly Done** |
| Phase 2 — Core Modules + Portal | Days 11-24 | $400 | Not Started | **In Progress** |
| Phase 3 — Content + Portals | Days 25-36 | $400 | Not Started | Not Started |
| Phase 4 — Reports + Communication | Days 37-46 | $400 | Not Started | Not Started |
| Phase 5 — Testing & Handover | Days 47-50 | $200 | Not Started | Not Started |

### Phase 1 — Foundation & Setup (Days 1-10) | $600

| # | Task | Days | Tracker Status | Actual Status | Notes |
|---|------|------|---------------|---------------|-------|
| 1.1 | Odoo 19 Enterprise -> Community Conversion | 3 | **Approved** | **DONE** | Running Odoo 19 Community on server |
| 1.2 | Student Profile — All Fields, Smart Buttons, Tabs | 3 | **Approved** | **DONE** | 64 models, full student form |
| 1.3 | Guardian Profile — All Fields, Smart Buttons | 2 | **Done** | **DONE** | Awaiting client review |
| 1.4 | Portal Setup + JWT Auth (All 4 User Types) | 2 | **Done** | **PARTIAL** | Parent login works; Student/Teacher/Admin login NOT yet separate |

**Phase 1 Actual: ~85% complete** (auth for all 4 user types still needs work)

### Phase 2 — Core Modules + Portal (Days 11-24) | $400

| # | Task | Days | Tracker Status | Actual Status | Notes |
|---|------|------|---------------|---------------|-------|
| 2.1 | Subscriptions, Discounts & Auto-Invoicing | 2 | **In Progress** | **DONE** | Financial plans, discounts, account.move invoices, cron |
| 2.2 | Admission & Registration Module | 2 | Not Started | **DONE (Odoo)** | Pipeline, documents, auto-enrollment all built |
| 2.3 | Attendance + Employee Enhancements | 2 | Not Started | **DONE (Odoo)** | Check-in/out, shifts, batch payroll, loans, penalties |
| 2.4 | Parent Self-Signup + Approval Flow **[NEW]** | 2 | Not Started | **NOT DONE** | No registration endpoint or UI |
| 2.5 | Paymob Integration + Cart + Checkout **[NEW]** | 2 | Not Started | **NOT DONE** | No Paymob SDK, checkout is static placeholder |
| 2.6 | Admin Dashboard — Core Screens **[NEW]** | 2 | In Progress | **PARTIAL (~60%)** | Dashboard + Students + Parents + Subscriptions + Invoices pages DONE with real API data. Remaining: Teachers, Attendance, Content, Kids Area, Messages, Reports, Settings pages |
| 2.7 | Portal: Parent Dashboard + Academic View | 2 | Not Started | **PARTIAL** | Dashboard + children + payments work; attendance calendar, grades, goals NOT wired |

**Phase 2 Actual: ~45% complete** (Odoo backend done, portal features lagging)

### Phase 3 — Content + Portals (Days 25-36) | $400

| # | Task | Days | Tracker Status | Actual Status | Notes |
|---|------|------|---------------|---------------|-------|
| 3.1 | Student Portal Screens **[NEW]** | 2 | Not Started | **NOT DONE** | No student login or screens |
| 3.2 | Teacher Portal Screens **[NEW]** | 2 | Not Started | **NOT DONE** | No teacher login or screens |
| 3.3 | Content Access Control + Library | 2 | Not Started | **DONE (Odoo)** | Models + access + usage tracking built |
| 3.4 | Kids Area Module + Booking | 2 | Not Started | **DONE (Odoo)** | Services, slots, bookings, attendance, packages built |
| 3.5 | AI Voice Recognition Integration | 2 | Not Started | **PARTIAL** | Backend API exists, no frontend game UI |
| 3.6 | REST API — All Endpoints Finalized | 2 | Not Started | **PARTIAL** | ~50% endpoints done (parent side mostly complete) |

**Phase 3 Actual: ~30% complete** (Odoo models built, portal screens and full API missing)

### Phase 4 — Reports + Communication (Days 37-46) | $400

| # | Task | Days | Tracker Status | Actual Status | Notes |
|---|------|------|---------------|---------------|-------|
| 4.1 | Academic & Student Reports (14) | 2 | Not Started | **PARTIAL** | ~4 of 14 built |
| 4.2 | Goals, Assessments & Course Reports (15) | 2 | Not Started | **PARTIAL** | ~1 of 15 built |
| 4.3 | Financial & Inventory Reports (8) | 2 | Not Started | **PARTIAL** | ~3 of 8 built |
| 4.4 | HR, Kids Area, Communication Reports (13) | 2 | Not Started | **PARTIAL** | ~2 of 13 built |
| 4.5 | Portal: Communication Features | 2 | Not Started | **PARTIAL** | Backend models done, portal UI not wired |

**Phase 4 Actual: ~20% complete** (10 of 50 reports exist, communication backend only)

### Phase 5 — Testing & Handover (Days 47-50) | $200

| # | Task | Days | Tracker Status | Actual Status | Notes |
|---|------|------|---------------|---------------|-------|
| 5.1 | End-to-End Integration Testing | 1 | Not Started | **NOT DONE** | |
| 5.2 | Bug Fixes, UI Polish, RTL Testing | 2 | Not Started | **NOT DONE** | |
| 5.3 | Documentation + Deployment + Handover | 1 | Not Started | **PARTIAL** | Odoo deployed to server, portal NOT deployed to production |

**Phase 5 Actual: ~5%**

### New Features Added in v2.0

| # | Feature | Phase | Status | Description |
|---|---------|-------|--------|-------------|
| 1 | Paymob Payment Integration | Phase 2 | **NOT DONE** | Cards + Mobile Wallets |
| 2 | Parent Self-Signup | Phase 2 | **NOT DONE** | Registration + verification + admin approval |
| 3 | Student Portal (Separate Login) | Phase 3 | **NOT DONE** | Own login for games, books, homework, grades, chat |
| 4 | Teacher Portal | Phase 3 | **NOT DONE** | Attendance, assignments, assessments, goals, messages |
| 5 | Admin Dashboard | Phase 2 | **NOT DONE** | Full control panel (users, content, billing) |
| 6 | 4 User Types Auth | Phase 1 | **PARTIAL** | Parent works; Student/Teacher/Admin need separate flows |

---

## 4. Odoo Backend — Detailed Module Status

### 4.1 Enterprise to Community Conversion — DONE
- Running Odoo 19 Community (`odoo:19.0` Docker image)
- Server: 168.231.124.49 | Container: `o19_web` / `o19_db`
- Database: `dar_elanwar`

### 4.2 Student Profile — DONE
- Model: `res.partner` (inherited) + student fields
- All fields: National ID, Admission Time, Status, Religion, Birth Place, Code, Arabic Name, Birthdate, Age, Gender, Birth Order
- Smart buttons: Subscriptions, Payments, Installments, Portal User
- Tabs: Study Plans, Financial Plans
- States: draft, pending, enrolled, suspended, graduated, archived
- Guardian links: `father_id`, `mother_id`

### 4.3 Guardian Profile — DONE
- Model: `res.partner` (inherited) with `is_guardian` flag
- Fields: Nationality, Education Level, Mother details, ID Number, Workplace, Job Number, City
- Smart buttons: Children count, Invoices, Payments, Balance, Attendance
- Portal user link

### 4.4 Subscriptions, Billing & Discounts — DONE
- `education.discount` — sibling, early_payment, scholarship, custom; percentage/fixed
- `education.subscription.type` — per department/level
- `education.student.subscription` — full lifecycle with discount integration
- `education.installment` — per-subscription with payment tracking
- `education.payment` + `education.payment.receipt`
- `education.financial.plan` + lines — discount fields, `account.move` invoice generation, daily cron
- Multiple subscriptions per student

### 4.5 Admission & Registration Module — DONE
- `education.admission.application` — pipeline: Application -> Assessment -> Accepted -> Enrolled
- Document tracking, auto-creates student on enrollment

### 4.6 Attendance — DONE
- `education.attendance` + `education.attendance.line`
- Status: present, absent, late, excused, on_leave
- Department/branch fields, check-in/check-out

### 4.7 Employee & Teacher — DONE
- Full employee profile with shift type, class assignment
- Attendance, salary (with bonuses/deductions), penalties, complaints, loans
- Batch payroll wizard

### 4.8 Kids Area Module — DONE
- Services, slots, bookings (with QR), attendance, packages

### 4.9 Content Management — DONE
- Categories (books, games, courses, videos), items with pricing/DRM
- Access control per student, usage tracking

### 4.10 Portal User Management — DONE
- `dar.portal.user` with password hashing, login tracking
- Manage from Odoo: create, activate, deactivate

### 4.11 Reports — 10 of 50 DONE

**Built (10 QWeb PDF Reports):**

| # | Report | File |
|---|--------|------|
| 1 | Student Details | `report_student_details.xml` |
| 2 | Student Statistics | `report_student_statistics.xml` |
| 3 | Attendance | `report_attendance.xml` |
| 4 | Financial | `report_financial.xml` |
| 5 | Employee | `report_employee.xml` |
| 6 | Evaluation Goals | `report_goals.xml` |
| 7 | Kids Area | `report_kids_area.xml` |
| 8 | Inventory | `report_inventory.xml` |
| 9 | Communication | `report_communication.xml` |
| 10 | Course | `report_course.xml` |

**Remaining: 40 reports across 4 categories:**
- Academic & Student Reports: ~10 remaining of 14
- Goals/Assessment Reports: ~14 remaining of 15
- Financial Reports: ~7 remaining of 8
- HR/Communication Reports: ~9 remaining of 13

---

## 5. Portal — Feature Status by User Type

### 5.1 Parent Portal

| Feature | Status | Details |
|---------|--------|---------|
| Login (phone + password) | **DONE** | JWT auth, memory-only token, auto-refresh |
| Dashboard | **DONE** | Children cards, balance, notifications |
| Children list & profiles | **DONE** | API-integrated via `useChildrenStore` |
| Billing & invoices | **PARTIAL** | Invoices, subscriptions, installments work; receipt download needs backend |
| Attendance calendar | **NOT DONE** | API exists, UI not wired |
| Grades & assessments | **NOT DONE** | Not wired |
| Goals & progress | **NOT DONE** | Not wired |
| Content store (browse) | **PLACEHOLDER** | Static UI, not connected to API |
| Cart & checkout | **PLACEHOLDER** | Hardcoded items, fake payment |
| Paymob payment | **NOT DONE** | No SDK, no integration |
| Kids Area booking | **PARTIAL** | Page exists, API configured, UI not fully wired |
| Communication | **PARTIAL** | Page exists, API configured, UI not wired |
| Self-signup & approval | **NOT DONE** | No registration endpoint or UI |
| Create child account | **NOT DONE** | Backend model exists |
| Password reset | **PARTIAL** | UI exists, needs backend endpoint |

### 5.2 Student Portal — NOT DONE (0%)
- No separate student login
- No student dashboard
- No content viewing (games, books, videos)
- No academic info (attendance, homework, grades, goals)
- No chat with teacher

### 5.3 Teacher Portal — NOT DONE (0%)
- No teacher login
- No teacher dashboard
- No attendance marking UI
- No assignment management UI
- No assessment recording UI
- No messaging UI

### 5.4 Admin Portal Dashboard — PARTIAL (~60%)

**DONE:**
- [x] Admin user type (`user_type` field on `dar.portal.user` — supports parent/admin/teacher/student)
- [x] Admin JWT authentication (`admin_jwt_required` decorator, `user_type` in token)
- [x] Admin login + redirect (admin users redirect to `/admin`, parents to `/dashboard`)
- [x] Admin layout (sidebar with logo, top bar, responsive mobile menu)
- [x] Dashboard page — real stats: student/parent/teacher counts, active subscriptions, total revenue, attendance rate, subscription breakdown, invoice breakdown, recent students, today summary
- [x] Students page — paginated list with search, department filter, status filter, attendance bars
- [x] Parents page — paginated list with search, phone/email/relation/children count/balance
- [x] Subscriptions page — paginated list with search, status filter, amounts (total/paid/remaining)
- [x] Invoices page — paginated list with search, status filter (paid/pending/draft/overdue), amounts

**API Endpoints (all `@admin_jwt_required`):**
- [x] `GET /api/admin/dashboard` — full dashboard stats
- [x] `GET /api/admin/students` — paginated with search/filters
- [x] `GET /api/admin/parents` — paginated with search
- [x] `GET /api/admin/subscriptions` — paginated with search/status
- [x] `GET /api/admin/invoices` — paginated with search/status

**NOT DONE:**
- [ ] Teachers management page
- [ ] Attendance management page
- [ ] Content management page
- [ ] Kids Area management page
- [ ] Messages management page
- [ ] Reports/export page
- [ ] Settings page
- [ ] CRUD operations (create/edit/delete) — currently read-only lists

---

## 6. REST API Endpoints Status

### 6.1 Authentication
| Endpoint | Method | Status |
|----------|--------|--------|
| `/api/auth/login` | POST | **DONE** |
| `/api/auth/refresh` | POST | **DONE** |
| `/api/auth/profile` | GET | **DONE** |
| `/api/auth/password` | POST | **DONE** |
| `/api/auth/forgot-password` | POST | **DONE** |
| `/api/auth/register` | POST | NOT DONE |
| `/api/auth/verify` | POST | NOT DONE |

### 6.2 Parent Endpoints — Mostly DONE
| Endpoint | Method | Status |
|----------|--------|--------|
| `/api/children` | GET | **DONE** |
| `/api/children/{id}` | GET | **DONE** |
| `/api/children/{id}/siblings` | GET | **DONE** |
| `/api/attendance/{id}` | GET | **DONE** |
| `/api/attendance/{id}/summary` | GET | **DONE** |
| `/api/invoices` | GET | **DONE** |
| `/api/invoices/{id}` | GET | **DONE** |
| `/api/payments` | GET, POST | **DONE** |
| `/api/payments/balance` | GET | **DONE** |
| `/api/payments/summary` | GET | **DONE** |
| `/api/subscriptions` | GET | **DONE** |
| `/api/subscriptions/{id}` | GET | **DONE** |
| `/api/parent/children/{id}/create-account` | POST | NOT DONE |

### 6.3 Student Endpoints — NOT DONE
All 7 endpoints (`/api/student/*`) not implemented.

### 6.4 Teacher Endpoints — NOT DONE
All 5 endpoints (`/api/teacher/*`) not implemented.

### 6.5 Admin Endpoints — PARTIAL (5 of 11)
| Endpoint | Method | Status |
|----------|--------|--------|
| `/api/admin/dashboard` | GET | **DONE** |
| `/api/admin/students` | GET | **DONE** |
| `/api/admin/parents` | GET | **DONE** |
| `/api/admin/subscriptions` | GET | **DONE** |
| `/api/admin/invoices` | GET | **DONE** |
| `/api/admin/teachers` | GET | NOT DONE |
| `/api/admin/attendance` | GET, POST | NOT DONE |
| `/api/admin/content` | GET, POST, PUT | NOT DONE |
| `/api/admin/kidsarea` | GET, POST | NOT DONE |
| `/api/admin/users` | GET, POST, PUT | NOT DONE |
| `/api/admin/reports` | GET | NOT DONE |

### 6.6 E-Commerce & Payment — NOT DONE
| Endpoint | Method | Status |
|----------|--------|--------|
| `/api/content/categories` | GET | **DONE** |
| `/api/content/items` | GET | **DONE** |
| `/api/content/items/{id}` | GET | **DONE** |
| `/api/cart` | GET, POST, DELETE | NOT DONE |
| `/api/checkout` | POST | NOT DONE |
| `/api/webhooks/paymob` | POST | NOT DONE |

### 6.7 Other Endpoints — Mostly DONE
Kids area (5 endpoints), messages (4 endpoints), config (3 endpoints), voice (2 endpoints) — all **DONE**.

**API Summary: ~32 of ~50 endpoints done (~64%)**

---

## 7. AI Voice Recognition

**STATUS: PARTIAL**
- [x] Backend API: `/api/voice/evaluate`, `/api/voice/words`
- [ ] Frontend game UI with microphone
- [ ] Web Speech API + Vosk (offline fallback)
- [ ] Arabic + English language support
- [ ] Scoring with celebration/encouragement

---

## 8. Overall Progress Summary

### By System

| System | Completion | Details |
|--------|-----------|---------|
| Odoo Backend Models | **95%** | 64 models, all major modules built |
| Odoo Views & Menus | **95%** | 20 view files, complete menu structure |
| Odoo Security/ACL | **95%** | 200+ access rules, 6 user groups |
| REST API Controllers | **64%** | ~32 of ~50 endpoints done (parent + admin dashboard/lists) |
| QWeb Reports | **20%** | 10 of 50 reports built |
| Portal - Public Pages | **90%** | 18 public pages with full UI |
| Portal - Parent Features | **50%** | Login, dashboard, children, payments; missing Paymob/cart |
| Portal - Student Features | **0%** | No student login or screens |
| Portal - Teacher Features | **0%** | No teacher login or screens |
| Portal - Admin Dashboard | **60%** | Dashboard + Students + Parents + Subscriptions + Invoices with real data. Remaining: 7 pages + CRUD |
| Paymob Integration | **0%** | Not started |
| AI Voice Recognition | **10%** | Backend endpoint only |

### By Task Tracker Phase

| Phase | Budget | Tasks Done | Completion | Key Remaining |
|-------|--------|-----------|-----------|---------------|
| Phase 1: Foundation | $600 | 3.5 of 4 | **85%** | Multi-user-type auth |
| Phase 2: Core + Portal | $400 | 3.5 of 7 | **50%** | Self-signup, Paymob, admin dashboard (partial), parent academic views |
| Phase 3: Content + Portals | $400 | 2 of 6 | **30%** | Student portal, teacher portal, API completion |
| Phase 4: Reports + Comms | $400 | 0 of 5 | **20%** | 40 reports, communication portal UI |
| Phase 5: Testing | $200 | 0 of 3 | **5%** | Full testing, docs, deployment |

### Overall Project: **~42% Complete**

---

## 9. Remaining Work — Priority Order

### IMMEDIATE (Complete Phase 1 & Phase 2)

1. **Task 2.4 — Parent Self-Signup + Approval [NEW]** (2 days)
   - `/api/auth/register` endpoint
   - Email/SMS verification
   - Admin approval workflow in Odoo
   - Registration UI in portal

2. **Task 2.5 — Paymob Integration + Cart + Checkout [NEW]** (2 days)
   - Paymob SDK + payment intent
   - Card + mobile wallet flows
   - Webhook handler -> Odoo invoice
   - Content auto-unlock

3. **Task 2.6 — Admin Dashboard Core Screens [NEW]** (2 days)
   - Admin login + role-based access
   - User management (CRUD students, guardians, teachers)
   - Content + billing management screens

4. **Task 2.7 — Parent Dashboard + Academic View** (2 days)
   - Wire attendance calendar to API
   - Wire grades/assessments display
   - Wire goals/progress display

### NEXT (Phase 3)

5. **Task 3.1 — Student Portal Screens [NEW]** (2 days)
   - Student login (separate JWT flow)
   - Dashboard, games, books, attendance, homework, grades, chat

6. **Task 3.2 — Teacher Portal Screens [NEW]** (2 days)
   - Teacher login
   - Attendance marking, assignments, assessments, messaging

7. **Task 3.3 — Content Access Control + Library** (2 days)
   - Wire portal content pages to API
   - DRM-lite protection

8. **Task 3.4 — Kids Area Booking Portal** (2 days)
   - Browse slots, book, pay, QR confirm

9. **Task 3.5 — AI Voice Recognition Frontend** (2 days)
   - Game UI + microphone + Web Speech API

10. **Task 3.6 — REST API Finalization** (2 days)
    - Complete all remaining endpoints
    - Postman collection

### THEN (Phase 4 + 5)

11. **Tasks 4.1-4.4 — 40 Remaining Reports** (8 days)
12. **Task 4.5 — Communication Portal** (2 days)
13. **Tasks 5.1-5.3 — Testing, Polish, Docs, Deploy** (4 days)

---

## 10. Scope Boundaries

| IN SCOPE | OUT OF SCOPE |
|----------|-------------|
| Odoo 19 backend (all modules) | Mobile native app (iOS/Android) |
| Portal (Parent, Student, Teacher, Admin) | Zoom/Google Meet integration |
| Parent self-signup | Game logic/animation development |
| Student separate login | Content creation (assets) |
| Paymob payment (cards + wallets) | Paymob account setup fees |
| REST API (all endpoints) | SMS gateway subscription |
| 50 QWeb reports | Server hosting costs |
| AI Voice Recognition | |
| Kids Area booking + payment | |
| Bidirectional sync (Portal <-> Odoo) | |

---

## 11. Technical Stack

### Odoo Backend
- **Framework:** Odoo 19 Community | **Language:** Python 3 | **DB:** PostgreSQL 16
- **Deployment:** Docker (`odoo:19.0` + `postgres:16`)
- **Auth:** JWT (PyJWT) | **Module:** `dar_elanwar` v19.0.6.0.0
- **Models:** 64 | **Views:** 20 XML | **Reports:** 10 QWeb PDF
- **Security:** 200+ ACL rules, 6 groups | **Dependencies:** base, mail, web, account

### Vue.js Portal
- **Framework:** Vue 3 Composition API | **Bundler:** Vite 5.4
- **Routing:** Vue Router 4.3 | **State:** Pinia 2.1 | **HTTP:** Axios 1.6
- **Styling:** Tailwind CSS 3.4
- **Pages:** 29 routes (18 public, 7 auth, 2 cart, 2 guest) | **Components:** 6

### Infrastructure
- **Server:** 168.231.124.49
- **Repo (Odoo + full project):** github.com/moaaznaabilali/dar-alanwar (private)
- **Repo (Portal only):** github.com/CityArtSolution/Dar-alanwar2026

---

## 12. Payment Schedule

| # | Milestone | Day | Amount | Status |
|---|-----------|-----|--------|--------|
| 1 | Phase 1: Foundation complete | 10 | $600 | Pending review |
| 2 | Phase 2: Payments + Admin core | 24 | $400 | Not started |
| 3 | Phase 3: Student/Teacher portals + Kids Area | 36 | $400 | Not started |
| 4 | Phase 4: Reports + Communication | 46 | $400 | Not started |
| 5 | Phase 5: Testing + Handover | 50 | $200 | Not started |

---

*Last updated: March 12, 2026*
