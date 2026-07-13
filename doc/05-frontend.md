# 05 — Frontend

The public site is **server-rendered Django templates** with Bootstrap and jQuery. There is no React/Vue SPA and no frontend package manager in this repo.

## Template hierarchy

Base layout: [`templates/base.html`](../templates/base.html)

Page templates typically `{% extends "base.html" %}` and fill blocks for title, content, and page-specific assets.

| Template | Used by |
|----------|---------|
| `templates/base.html` | Shared chrome (nav, footer, CSS/JS includes) |
| `templates/index.html` | Home |
| `templates/packages.html` | Package list |
| `templates/package_details.html` | Package detail |
| `templates/about.html` | About |
| `templates/contact.html` | Contact |
| `templates/blog.html` | Blog list |
| `templates/blog_detail.html` | Blog detail |
| `templates/emails/contact_notification.html` | Admin email |
| `templates/emails/contact_confirmation.html` | Customer email |

**Alternate / unused paths:** `templates/packages/package_list.html` and `package_detail.html` exist as leftovers; views point at the root-level names above.

**Missing:** `templates/packages/search_results.html` is expected by `search_packages` but is not in the repo.

## Route → view → template

| Route | View | Template |
|-------|------|----------|
| `/` | `home` | `index.html` |
| `/packages/` | `PackageListView` | `packages.html` |
| `/package/<pk>/` | `PackageDetailView` | `package_details.html` |
| `/search/` | `search_packages` | `packages/search_results.html` (missing) |
| `/about/` | `about` | `about.html` |
| `/contact/` | `contact` | `contact.html` (GET); JSON on POST |
| `/blog/` | `blog` | `blog.html` |
| `/blog/<slug>/` | `blog_detail` | `blog_detail.html` (GET); JSON on POST |

URL names use the `packages:` namespace (e.g. `{% url "packages:contact" %}`).

## Static assets

| Path | Role |
|------|------|
| `static/css/` | Bootstrap, theme CSS, page-specific sheets (offers, packages, team, inclusions, etc.) |
| `static/js/` | jQuery, Bootstrap, Swiper, WOW, Magnific Popup, `main.js` |
| `static/scss/` | Theme SCSS sources (`main.scss` + partials) |
| `static/img/`, fonts, webfonts | Images and icon fonts |

In development, Django serves files from `STATICFILES_DIRS` (`static/`). In production, `collectstatic` + WhiteNoise serve compressed static files.

### `pages/` vs `static/`

[`pages/`](../pages/) is a **standalone HTML theme kit** (demo pages, sometimes including `.php` contact stubs). It is **not** included in Django URL patterns. Use it only as a visual reference when rebuilding sections. Runtime assets belong under `static/` and templates under `templates/`.

### SCSS workflow

There is no `package.json` or committed Sass build pipeline. If you edit SCSS, compile to CSS with your local Sass tooling and commit the updated CSS under `static/css/`, or introduce a documented Node build step as a deliberate project change.

## Filtering and search (HTML forms / query strings)

Package list accepts GET params (handled in `PackageListView`):

- `category` — category id
- `type` — package type
- `min_price` / `max_price`
- `q` — text search on name/description/location/destinations

Prefer `/packages/?q=...` until the dedicated search template exists.

## AJAX form pattern

Contact and blog comments use browser `fetch` with CSRF:

1. Read CSRF token from cookie / form field.
2. `POST` `FormData` to the Django URL.
3. Expect JSON: `{ "success": true }` or `{ "success": false, "error": "..." }`.
4. Contact may also return `email_error` when the DB save succeeded but SMTP failed.

Always preserve CSRF middleware behavior when changing these forms.

## Templatetags

[`packages/templatetags/currency_format.py`](../packages/templatetags/currency_format.py) provides `inr_commas` for Indian-style number formatting in templates:

```django
{% load currency_format %}
{{ package.price|inr_commas }}
```

## JavaScript role

[`static/js/main.js`](../static/js/main.js) drives UI behavior (sliders, sticky headers, animations). It is not an application state layer. New interactive features should either:

- Stay in small page-local scripts, or
- Be documented clearly if a larger JS module is introduced.

## Frontend conventions for new pages

1. Extend `base.html`.
2. Keep one primary purpose per page section.
3. Pull dynamic content from view context / ORM — avoid hardcoding package lists in HTML.
4. Reuse existing CSS classes from the theme before inventing parallel design systems.
5. Test desktop and mobile widths; the theme is Bootstrap-based and responsive.
