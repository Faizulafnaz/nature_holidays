# 06 — Admin / CMS

Content is managed through Django admin at **`/admin/`**, styled with **django-unfold**. Registration and UX live in [`packages/admin.py`](../packages/admin.py).

## Access

1. Create a staff user: `python manage.py createsuperuser`
2. Open `/admin/` and sign in
3. Only staff/superusers can access admin; the public site has no login

On Render, optional env vars `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, and `DJANGO_SUPERUSER_PASSWORD` can bootstrap a superuser during [`build.sh`](../build.sh).

## Unfold conventions

Admins subclass `unfold.admin.ModelAdmin` and use Unfold widgets via `UNFOLD_FORMFIELD_OVERRIDES` (text inputs, textareas, selects, boolean switches). Prefer the same pattern when registering new models so the UI stays consistent.

## Package editing (most important workflow)

`PackageAdmin` uses tabbed fieldsets and inlines:

| Inline | Manages |
|--------|---------|
| `PackageImageInline` | Gallery images |
| `ItineraryInline` | Day-by-day plan |
| `PackageInclusionInline` | Inclusions |
| `PackageExclusionInline` | Exclusions |

**Fieldset groups:** Package Details → Pricing & Capacity → Toggles (`is_featured`, `is_popular`, `is_active`).

### Checklist: publish a new package

1. Ensure a `Category` (and optional `Offer`) exists.
2. Create `Package` with cover image, price, duration, location, destinations.
3. Set `is_active=True`. Optionally `is_featured` / `is_popular` for homepage placement.
4. Add itinerary days (unique day numbers per package).
5. Add inclusions / exclusions with sensible `order`.
6. Add gallery images if needed.
7. Verify on `/packages/` and `/package/<id>/`.

## Blog workflow

- `BlogCategory` / `BlogTag` — slugs auto-populate from name.
- `BlogAdmin` — content, classification, publication tabs; `BlogCommentInline` for moderation.
- Set `status=published` and `is_active=True` for public visibility.
- `views_count` is read-only (incremented by the detail view).

### Checklist: publish a blog post

1. Create category/tags as needed.
2. Write title (slug auto-fills), excerpt, content, featured image.
3. Set status to **Published**, set `published_date` if required by your process.
4. Confirm at `/blog/` and `/blog/<slug>/`.
5. Moderate comments under Blog → Comments or the inline on the post.

## Lead and contact management

`ContactAdmin`:

- List shows name, email, phone, service, flags `is_read` / `is_replied` (editable in list).
- Use these flags to track follow-up; they do not email the customer automatically when toggled.

## Homepage / marketing content

| Admin model | Effect on site |
|-------------|----------------|
| Featured / popular packages | Driven by package toggles |
| `Offer` | Home offers section; package discounted price when linked |
| `TeamMember` | Home + about |
| `SiteStats` | Home counters (`objects.first()` — keep a single meaningful row) |
| `InstagramPost` | Home slider; `order` controls sequence; `link` opens Instagram URL |
| `NewsletterSubscription` | Stored emails only — **no public signup endpoint yet** |
| `CTASection` | Editable in admin; **not clearly consumed by main public views** — wire a view/template before relying on it for campaigns |

## Moderation tips

- Soft-hide content with `is_active=False` instead of deleting when possible.
- Deactivate spam blog comments via `is_active`.
- Prefer Cloudinary-ready image sizes; large uploads slow admin and pages.

## Extending admin

When adding a model:

1. Register with `ModelAdmin` + Unfold overrides.
2. Add `list_display`, `list_filter`, `search_fields` early.
3. Use inlines for tightly coupled child rows (like package itineraries).
4. Use `prepopulated_fields` for slugs.
5. Document any new model that is admin-only until a public view exists (same pattern as newsletter / CTA).
