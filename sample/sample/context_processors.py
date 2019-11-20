from django.conf import settings


def global_settings(request):
    return {
        'CACHE_TIMEOUT': settings.CACHES["default"]["TIMEOUT_1H"],
    }
