# Dar Al-Anwar Educational Management System

Complete educational institution management system built on Odoo 19 Community with a Nuxt.js parent portal.

## Project Structure

```
dar-alanwar/
├── odoo-addons/dar_elanwar/   # Custom Odoo addon
├── parent-portal/              # Nuxt.js SSR portal
└── deploy/nginx/               # nginx config snippet
```

## Server Setup (Native)

- **Odoo 19 Community** on port `8071` (systemd service)
- **PostgreSQL** on port `5433` (separate cluster)
- **Nuxt Portal** on port `3000` (PM2)
- **nginx** reverse proxy for `/portal/` and `/api/`

## URLs

- **Odoo**: `http://168.231.124.49:8071/web`
- **Portal**: `http://168.231.124.49/portal/`
- **API**: `http://168.231.124.49/api/`

## Login

- Username: `h`
- Password: `admin`
