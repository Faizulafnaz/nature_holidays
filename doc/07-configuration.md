# 07 — Configuration

Configuration uses **python-decouple** and environment variables. Local developers copy [`env_template.txt`](../env_template.txt) to `.env`. Production (Render) sets the same keys in the dashboard.

**Never commit `.env` or real secrets.**

## Settings modules

| File | Role |
|------|------|
| [`nature_holidays/settings.py`](../nature_holidays/settings.py) | Entry point; if `DJANGO_ENV=production`, imports production module; otherwise defines development settings |
| [`nature_holidays/settings_production.py`](../nature_holidays/settings_production.py) | Full production configuration |

```bash
DJANGO_ENV=development   # default if unset
DJANGO_ENV=production    # Render / live
```

## Environment variable reference

### Core Django

| Variable | Dev typical | Prod typical | Purpose |
|----------|-------------|--------------|---------|
| `DJANGO_ENV` | `development` | `production` | Settings selection |
| `SECRET_KEY` | any long random string | strong unique secret | Django crypto signing |
| `DEBUG` | `True` | `False` | Debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | your domain(s) | Host header allowlist |
| `CSRF_TRUSTED_ORIGINS` | `http://localhost:8000,...` | `https://your-domain` | Trusted CSRF origins |
| `RENDER_EXTERNAL_HOSTNAME` | — | `your-service.onrender.com` | Extra allowed host on Render |

### Database

| Variable | Dev | Prod |
|----------|-----|------|
| `DATABASE_URL` | Unused (SQLite file) | Postgres URL from Render |

Production parses `DATABASE_URL` with `dj-database-url`.

### Cloudinary (media)

| Variable | Required in prod | Purpose |
|----------|------------------|---------|
| `CLOUDINARY_CLOUD_NAME` | Yes | Cloud name |
| `CLOUDINARY_API_KEY` | Yes | API key |
| `CLOUDINARY_API_SECRET` | Yes | API secret |

In development, if any of these are missing, media falls back to local `FileSystemStorage` under `media/`.

### Email (SMTP)

| Variable | Purpose |
|----------|---------|
| `EMAIL_HOST` | Default `smtp.gmail.com` |
| `EMAIL_PORT` | Default `587` |
| `EMAIL_USE_TLS` | Default `True` |
| `EMAIL_HOST_USER` | SMTP username (Gmail address) |
| `EMAIL_HOST_PASSWORD` | Gmail **app password**, not account password |
| `DEFAULT_FROM_EMAIL` | From header |
| `ADMIN_EMAIL` | Recipient for contact notifications |

### Optional build bootstrap (Render)

| Variable | Purpose |
|----------|---------|
| `DJANGO_SUPERUSER_USERNAME` | Create/update staff superuser in `build.sh` |
| `DJANGO_SUPERUSER_EMAIL` | Superuser email |
| `DJANGO_SUPERUSER_PASSWORD` | Superuser password |

All three must be set for the bootstrap block to run.

## Development vs production differences

| Concern | Development | Production |
|---------|-------------|------------|
| Database | SQLite `db.sqlite3` | PostgreSQL |
| Media | Local `media/` or optional Cloudinary | Cloudinary |
| Static | Served from `static/` by runserver | WhiteNoise + `STATIC_ROOT` after collectstatic |
| HTTPS | Usually HTTP localhost | HTTPS redirect, HSTS, secure cookies |
| Logging | Django defaults | Configured in production settings |
| Debug | Often `True` | Must be `False` |

## Timezone and i18n

Development settings use `TIME_ZONE = 'Asia/Kolkata'` and `LANGUAGE_CODE = 'en-us'`. Keep display and business logic consistent with IST unless the product expands internationally.

## Checklist before changing settings

1. Prefer env vars over hardcoding.
2. Mirror new required keys in `env_template.txt` and this doc.
3. Test both `DJANGO_ENV=development` and a production-like config when touching the settings switch.
4. After adding middleware or installed apps, update both settings paths if they diverge.
