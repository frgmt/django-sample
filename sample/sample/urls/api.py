from django.conf import settings
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    # enable login on the browsable API.
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns.append(
            path('__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass

if settings.REST_FRAMEWORK.get('ENABLE_DOCS', False):
    urlpatterns.append(
        path('docs/',
            get_swagger_view(urlconf=settings.SUBDOMAIN_URLCONFS[settings.SUBDOMAIN_API])
        ),
    )
