# Nature Holidays — Developer Documentation

This folder is the primary technical reference for developers working on Nature Holidays. The root [README.md](../README.md) is a product and deploy overview; these guides go deeper so you can onboard, change, and scale the system safely.

## Reading order

| # | Guide | When to read it |
|---|--------|-----------------|
| 1 | [Overview](01-overview.md) | First day — product purpose, stack, repo map |
| 2 | [Getting started](02-getting-started.md) | Local setup and everyday commands |
| 3 | [Architecture](03-architecture.md) | How requests flow through Django MVT |
| 4 | [Domain model](04-domain-model.md) | Entities, relationships, which pages they power |
| 5 | [Frontend](05-frontend.md) | Templates, static assets, AJAX forms |
| 6 | [Admin / CMS](06-admin-cms.md) | Unfold admin and content workflows |
| 7 | [Configuration](07-configuration.md) | Environment variables, dev vs prod |
| 8 | [Deployment](08-deployment.md) | Render, Cloudinary, email, smoke tests |
| 9 | [Scaling guide](09-scaling-guide.md) | How to grow this codebase without painting yourself into a corner |

## Quick facts

- **Stack:** Django 4.2 monolith, server-rendered Bootstrap templates, SQLite (dev) / PostgreSQL (prod)
- **App:** Single Django app `packages/`
- **CMS:** Django admin with django-unfold at `/admin/`
- **Hosting:** Render + Gunicorn + WhiteNoise + Cloudinary + Gmail SMTP
- **No REST API / SPA today** — classic Model–View–Template

## Git root

The git repository root is the `nature_holidays/` directory (where `manage.py` lives), not the parent Cursor workspace folder that may contain a local `venv/`.
