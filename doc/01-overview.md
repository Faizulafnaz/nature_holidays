# 01 — Overview

Nature Holidays is a travel and tourism marketing site for a Kerala-based operator. Staff manage packages, offers, blog posts, and leads through Django admin; visitors browse packages, read the blog, and submit contact inquiries.

## What the product does

| Area | Capability |
|------|------------|
| Packages | Categories, types (family/group/FIT/honeymoon/luxury), pricing, offers, itineraries, inclusions/exclusions, galleries |
| Home content | Featured/popular packages, offers, team, site stats, Instagram image slider |
| Blog | Categories, tags, published posts, public comments |
| Contact | Form → DB record + admin email + customer confirmation email |
| CMS | Staff-only Unfold admin at `/admin/` |

There is **no public user accounts system**, booking checkout, or payment integration today.

## Tech stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.12.8 (`runtime.txt`) |
| Framework | Django 4.2.7 |
| Admin UI | django-unfold |
| Frontend | Django templates + Bootstrap, jQuery, Swiper, WOW, Magnific Popup |
| Styles | CSS under `static/css/`; SCSS sources under `static/scss/` (no Node build in repo) |
| DB (dev) | SQLite (`db.sqlite3`) |
| DB (prod) | PostgreSQL via `DATABASE_URL` + `dj-database-url` + `psycopg` |
| Media (prod) | Cloudinary (`django-cloudinary-storage`) |
| Static (prod) | WhiteNoise |
| App server | Gunicorn → `nature_holidays.wsgi:application` |
| Config | python-decouple (`.env` / env vars) |
| Email | Gmail SMTP |
| Hosting | Render |

Dependencies are listed in [`requirements.txt`](../requirements.txt).

## Repository layout

```
nature_holidays/                 ← git root (manage.py lives here)
├── nature_holidays/             ← Django project package
│   ├── settings.py              ← Dev settings; switches on DJANGO_ENV
│   ├── settings_production.py   ← Production configuration
│   ├── urls.py                  ← Root URLconf
│   ├── wsgi.py / asgi.py
├── packages/                    ← Only Django app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   ├── templatetags/
│   └── management/commands/
├── templates/                   ← Server-rendered HTML
├── static/                      ← CSS, JS, images served by Django
├── pages/                       ← Static HTML theme kit (NOT wired to Django)
├── media/                       ← Local uploads (dev; gitignored)
├── doc/                         ← This documentation
├── build.sh                     ← Render build script
├── env_template.txt             ← Copy to .env
├── requirements.txt
└── README.md
```

### Important distinctions

- **`static/`** — runtime assets referenced by templates.
- **`pages/`** — original theme demo HTML. Useful as design reference only; Django does not serve these routes.
- **Workspace vs repo** — a parent folder may contain a local `venv/`; application code and git history live under this `nature_holidays/` directory.

## Public feature map (routes)

Defined in [`packages/urls.py`](../packages/urls.py), included from [`nature_holidays/urls.py`](../nature_holidays/urls.py):

| URL | Name | Purpose |
|-----|------|---------|
| `/` | `packages:home` | Homepage |
| `/packages/` | `packages:package_list` | Package listing + filters |
| `/package/<pk>/` | `packages:package_detail` | Package detail |
| `/search/` | `packages:search_packages` | Package search (see known gap below) |
| `/about/` | `packages:about` | About / team |
| `/contact/` | `packages:contact` | Contact form |
| `/blog/` | `packages:blog` | Blog listing |
| `/blog/<slug>/` | `packages:blog_detail` | Blog post + comments |
| `/admin/` | — | Staff CMS |

## Architecture at a glance

Classic Django **Model–View–Template** monolith. No SPA, no DRF REST API. Content is edited in admin, stored in the database, and rendered into HTML on each request. Contact and blog comments use small AJAX `JsonResponse` endpoints on the same views.

See [03-architecture.md](03-architecture.md) for request flow diagrams.

## Known gap

The search view renders `packages/search_results.html`, but that template is not present in the repo. Package filtering on `/packages/?q=...` works; standalone `/search/` will fail until the template is added. Tracked again in the [scaling guide](09-scaling-guide.md).
