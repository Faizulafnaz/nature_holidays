# 09 — Scaling guide

This guide is specific to **Nature Holidays as it exists today**: one Django app (`packages`), MVT templates, admin-driven CMS, Render hosting. Use it when the team grows, traffic grows, or features outgrow a single `views.py` / `models.py`.

## Principles

1. **Prefer boring, incremental change** over rewriting for a SPA or microservices until there is a concrete need.
2. **Ship tests before large refactors** — [`packages/tests.py`](../packages/tests.py) is currently an empty stub.
3. **Keep one source of truth for content** (Postgres + admin) unless you intentionally add an API consumer.
4. **Document admin-only models** until they have public views (newsletter, CTA today).

## Near-term fixes (do these first)

| Item | Why |
|------|-----|
| Add `templates/packages/search_results.html` (or point search at `packages.html`) | `/search/` is broken without it |
| Add smoke tests for home, package list/detail, contact POST, blog detail | Safer refactors |
| Add `select_related('category', 'offer')` / `prefetch_related` on package and blog querysets | Cuts N+1 queries as catalog grows |
| Wire or remove unused CMS pieces (`NewsletterSubscription` public form, `CTASection` on templates) | Avoids dead admin data |

## Code structure growth path

Current: almost all logic in `packages/views.py`, `packages/models.py`, `packages/admin.py`.

**When files become hard to navigate** (roughly: views ≫ 500–800 lines of mixed concerns, or multiple product domains), split by domain **inside the same app** first:

```text
packages/
  models/
    __init__.py      # re-export models for migrations compatibility
    package.py
    blog.py
    site.py
  views/
    home.py
    packages.py
    blog.py
    contact.py
  services/
    email.py         # contact notification / confirmation
    pricing.py       # offer price helpers if logic grows
```

Keep URL names stable (`packages:home`, etc.) so templates do not break.

**When to add a second Django app** (e.g. `bookings/`): a new bounded context with its own models lifecycle (orders, payments, customer accounts) that would clutter the marketing CMS.

## API and frontend strategy

| Situation | Recommendation |
|-----------|----------------|
| Marketing site only | Stay on Django templates |
| Need mobile app or separate JS frontend | Add Django REST Framework (or similar) under `/api/`, version it, keep admin as CMS |
| “Just add React for one page” | Avoid mixing without a clear boundary; either progressive enhancement with small JS or a deliberate API + frontend |

Do not invent a REST API “for the future” with no consumer — it doubles maintenance.

If you adopt a SPA later:

1. Define auth for API clients (session + CSRF for same-site, or token auth for mobile).
2. Keep media on Cloudinary.
3. Treat Unfold admin as the still-supported CMS unless you build a custom admin.

## Product feature roadmap (suggested order)

These align with ideas in the root README but with implementation notes for *this* codebase:

| Feature | Suggested approach |
|---------|-------------------|
| Fix search | Template or redirect; reuse list filters |
| Newsletter signup | Public POST view + CSRF; save `NewsletterSubscription`; optional double opt-in later |
| CTA sections | Load active `CTASection` in home/about context |
| Bookings | New models (`Booking`, status, package FK, customer fields); admin pipeline first, then public form |
| Payments | Integrate Stripe/PayPal **after** booking model exists; never store card data in Django models |
| Instagram API | Optional later; manual `InstagramPost` is fine at current scale |
| i18n | Django i18n + locale middleware when you have real translated copy |
| Advanced search | Postgres full-text first; Elasticsearch only if catalog/query complexity demands it |

## Data and performance

- **Indexes:** Add DB indexes on frequent filters (`Package.is_active`, `category`, `package_type`, `Blog.slug`, `Blog.status`) when query plans slow down.
- **Querysets:** Use `select_related` / `prefetch_related` on detail and list views; avoid per-category `.count()` loops on home if category count grows (annotate instead).
- **Images:** Upload reasonably sized images; use Cloudinary transformations for thumbnails on list pages.
- **Caching:** Start with Django’s cache framework + Redis on Render only after measuring; cache homepage fragments first.
- **Pagination:** Package and blog lists already paginate — keep page sizes modest.

## Operations and delivery

| Gap today | Scaling move |
|-----------|--------------|
| No CI | Add GitHub Actions: `pip install`, `manage.py check`, `manage.py test`, optional lint |
| No Docker | Optional later for parity; not required while Render build works |
| Manual deploys | Keep Render auto-deploy from `master`/`main`; protect production env vars |
| Logging | Production settings already configure logging — ship errors to a log drain or Sentry when traffic matters |
| Backups | Use Render Postgres backups; document restore steps for the team |

## Testing strategy

Before large changes, add:

1. **Model tests** — `get_offer_price()` with/without offer; slug uniqueness assumptions.
2. **View tests** — status codes for main routes; contact POST creates `Contact`.
3. **Admin smoke** — optional; lower priority than public views.

Run locally:

```bash
python manage.py test packages
```

## Frontend scale options

1. **Stay on Bootstrap theme** — fastest for a marketing site; extend `static/css` carefully.
2. **Introduce a Sass/npm build** — only if SCSS edits become frequent; document scripts in README.
3. **Gradual componentization** — Django template partials (`{% include %}`) before any JS framework.

Avoid a second parallel design system under `pages/` — treat `pages/` as reference only.

## Decision checklist for “should we rewrite?”

Rewrite or split services only if several are true:

- Multiple client apps need the same API
- Team size makes a monolith merge bottleneck *and* domains are cleanly separable
- Booking/payment compliance requires isolation you cannot get in-process
- Measured performance limits that caching and query fixes cannot address

Until then, **modular monolith** (clear packages/modules, tests, indexes) is the intended scale path.

## Related reading

- Architecture: [03-architecture.md](03-architecture.md)
- Domain model: [04-domain-model.md](04-domain-model.md)
- Deployment: [08-deployment.md](08-deployment.md)
