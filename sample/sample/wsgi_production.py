"""
WSGI config for sample project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings.production")

# If you are using a WSGI interface to serve your app,
# you can also apply a middleware which will ensure that
# you catch errors even at the fundamental level of your Django application.
# See http://raven.readthedocs.org/en/latest/config/django.html#wsgi-middleware
application = Sentry(get_wsgi_application())
