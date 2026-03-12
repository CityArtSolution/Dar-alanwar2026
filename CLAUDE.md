# Dar Al-Anwar Academy Management System

## Project Structure
```
dar-alanwar/
  odoo/dar_elanwar/       # Odoo 19 Community addon (Python)
  portal/                  # Vue.js 3 parent portal (Vite + Tailwind)
  DarAlAnwar_PRD_v4_STATUS.md  # Full PRD + task tracker status
```

## Odoo Module (`dar_elanwar`)
- **Version:** 19.0.6.0.0
- **Edition:** Community ONLY (never use Enterprise addons)
- **Dependencies:** base, mail, web, account
- **Models:** 64 | **Views:** 20 XML | **Reports:** 10 QWeb PDF | **API Controllers:** 14
- **Key:** `account` dependency added for financial plan invoice generation

### Manifest Load Order
The data file order in `__manifest__.py` matters:
1. Security files first
2. Data files (sequences, crons)
3. All view files with actions (subscription_views, discount_views, etc.)
4. `menu_views.xml` (references actions from above)
5. `portal_user_views.xml` (references menus from menu_views)
6. Reports last

### Deploy to Server (168.231.124.49)
```bash
rsync -avz odoo/dar_elanwar/ root@168.231.124.49:/odoo/dar_elanwar_custom_addons/dar_elanwar/
ssh root@168.231.124.49 "docker exec o19_web odoo -d dar_elanwar -u dar_elanwar --stop-after-init --no-http"
```

### Local Dev
```bash
cp -r odoo/dar_elanwar/ ~/Documents/projects/odoo19-apps/custom_addons/dar_elanwar/
docker exec odoo19-dev odoo -d odoo19_dev -u dar_elanwar --stop-after-init --no-http
```
Local Odoo at http://localhost:8079

## Portal (Vue.js)
- **Stack:** Vue 3 + Vite 5.4 + Tailwind 3.4 + Pinia 2.1 + Axios 1.6
- **Routes:** 29 (18 public, 7 auth, 2 cart, 2 guest)
- **Auth:** JWT in memory (not localStorage), auto-refresh on 401
- **API base:** `/api` (proxied to Odoo backend)

## Git & Repos
- **Full project:** github.com/moaaznaabilali/dar-alanwar (private)
- **Portal for team:** github.com/CityArtSolution/Dar-alanwar2026
- NEVER add Co-Authored-By Claude in commits
- All authorship: Moaaz Nabil only

## Current Status (March 12, 2026)
- **Task Tracker:** v2.0 | 29 tasks | 50 days | Phase 2 in progress
- **Overall:** ~38% complete
- **Done:** Odoo backend (95%), parent login/dashboard/payments, 10 reports
- **Not done:** Paymob, self-signup, student/teacher/admin portals, 40 reports
- See `DarAlAnwar_PRD_v4_STATUS.md` for full breakdown
