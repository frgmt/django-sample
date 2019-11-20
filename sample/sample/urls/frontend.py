from django.conf import settings
from django.urls import include, path
from django.views.defaults import server_error, page_not_found
from django.views.i18n import JavaScriptCatalog

from cache.decorators import cache_page
from main.views import PageNotFoundView

urlpatterns = [
    path('users/', include('users.urls.frontend')),
    path(
        'jsi18n/',
        cache_page(settings.CACHES["default"]["TIMEOUT_1H"])(JavaScriptCatalog.as_view(packages=['sample'])),
        name='jsi18n'
    ),
    path('', include('main.urls')),
]

handler404 = PageNotFoundView.as_view()

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
            path('500/', server_error),
            path('404/', page_not_found),
        ]
    except ImportError:
        pass
