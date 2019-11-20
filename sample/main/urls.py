from django.conf import settings
from django.urls import path

from cache.decorators import cache_page
from main.views import (
    IndexView,
)

FAVICON_PATH = getattr(settings, 'FAVICON_PATH')

urlpatterns = [
    path('', cache_page(settings.CACHES["default"]["TIMEOUT_1H"])(IndexView.as_view()), name="home"),
]
