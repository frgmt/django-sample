from django.urls import include, path
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    path('', admin.site.urls),
]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns.append(
            path('__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass
