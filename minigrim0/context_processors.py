from django.conf import settings


def plausible_url(request):
    """Add PLAUSIBLE_URL and DEBUG to template context."""
    return {
        'PLAUSIBLE_URL': getattr(settings, 'PLAUSIBLE_URL', None),
        'PLAUSIBLE_DOMAIN': getattr(settings, 'PLAUSIBLE_DOMAIN', None),
        'DEBUG': getattr(settings, 'DEBUG', False)
    }
