# 02 — Getting started

Set up a local development environment and run Nature Holidays on your machine.

## Prerequisites

- Python **3.12** (production pins `python-3.12.8` in `runtime.txt`)
- `pip` and a virtual environment tool
- Git
- Optional: Cloudinary credentials (only if you want cloud media locally)
- Optional: Gmail app password (only if you want real email locally)

## 1. Clone and enter the project

```bash
cd nature_holidays   # directory that contains manage.py
```

## 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```



## 3. Install dependencies

```bash
pip install -r requirements.txt
```



## 4. Configure environment

```bash
# Copy the template
cp env_template.txt .env
```

Edit `.env` for local work. Minimum useful values:

```bash
DJANGO_ENV=development
SECRET_KEY=change-me-to-a-long-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

- Leave Cloudinary empty to use local `media/` storage.
- Email settings can stay as placeholders; contact submissions still save to the DB if SMTP fails (see contact view behavior).

Never commit `.env`. It is gitignored.

Full variable reference: [07-configuration.md](07-configuration.md).

## 5. Migrate the database

Development uses SQLite at `db.sqlite3` in the project root.

```bash
python manage.py migrate
```



## 6. Create a superuser

```bash
python manage.py createsuperuser
```

Admin UI: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 7. Load sample data (optional)

```bash
python manage.py populate_sample_data

```

Creates sample categories, offers, packages, team members, blog posts, and related detail rows. Useful for UI work without hand-entering CMS content.

## 8. Run the development server

```bash
python manage.py runserver
```


| URL                                                                | What         |
| ------------------------------------------------------------------ | ------------ |
| [http://127.0.0.1:8000/](http://127.0.0.1:8000/)                   | Public site  |
| [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)       | Unfold admin |
| [http://127.0.0.1:8000/packages/](http://127.0.0.1:8000/packages/) | Package list |




## Everyday commands


| Task                                  | Command                                          |
| ------------------------------------- | ------------------------------------------------ |
| New model migrations                  | `python manage.py makemigrations` then `migrate` |
| Django shell                          | `python manage.py shell`                         |
| Collect static (rarely needed in dev) | `python manage.py collectstatic`                 |
| Sample data                           | `python manage.py populate_sample_data`          |
| Site media shells (hero + page media) | `python manage.py seed_site_media`               |




## Where files live locally


| Path           | Role                                                    |
| -------------- | ------------------------------------------------------- |
| `db.sqlite3`   | Dev database (gitignored)                               |
| `media/`       | Uploaded images when Cloudinary is not configured       |
| `static/`      | Source static files (`STATICFILES_DIRS`)                |
| `staticfiles/` | Collectstatic output (prod / local collect; gitignored) |
| `templates/`   | HTML templates                                          |




## Sanity checks after setup

1. Home page loads with packages/offers if sample data was loaded.
2. `/admin/` accepts your superuser login.
3. Create or edit a package in admin and confirm it appears on `/packages/`.
4. Submit the contact form; a `Contact` row should appear in admin (email may fail without real SMTP).
5. Site photos: in admin open **Hero Slides** and **Site Page Media** to upload hero / about / choose-us / breadcrumb images. Use **CTA Section** for the home CTA background. Until uploads exist, the site uses built-in static fallbacks.



## Next steps

- Understand request flow: [03-architecture.md](03-architecture.md)
- Learn the data model: [04-domain-model.md](04-domain-model.md)
- Deploy to Render: [08-deployment.md](08-deployment.md)

