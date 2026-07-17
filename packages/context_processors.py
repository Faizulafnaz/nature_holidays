from .models import SitePageMedia


def page_media(request):
    """Inject singleton SitePageMedia for breadcrumb / about / choose-us images."""
    try:
        media = SitePageMedia.objects.first()
    except Exception:
        media = None
    return {'page_media': media}
