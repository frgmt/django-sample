# -*- coding: utf-8 -*-
"""
Development environment is accessed over https, nearly same as
production.

You have to build ssl enviroment like below for using this setting.
if you don't want to build, use localhost_http.py

ex. ssl environment
 client - nginx - django runserver
"""

from os import environ
from .base import *
from .settings_base_credential import *


# STATIC_ROOT is required to run collectstatic locally.
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))


# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
########## END DEBUG CONFIGURATION


########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['sample.local', 'api.sample.local', 'managing.sample.local']
########## END HOST CONFIGURATION

########## SESSION CONFIGRATION
CSRF_COOKIE_DOMAIN = '.sample.local'
SESSION_COOKIE_DOMAIN = '.sample.local'
########## END DEBUG CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sample.db.backends.postgis',
        'NAME': ''.join([SITE_NAME, '_localhost']),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': environ.get('DB_HOST', ''),
        'PORT': '5432',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# RedisClient settings (using docker container)
REDIS_CLUSTER = 'sample-staging'
REDIS_PRIMARY_ENDPOINT = 'redis'
# Django Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default',
        'TIMEOUT': 24 * 60 * 60,
        'TIMEOUT_1H': 60 * 60,
        'VERSION': CACHE_VERSION
    }
}
# local redis version for docker container
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': [
#             'redis://{}:6379/0'.format(REDIS_PRIMARY_ENDPOINT),
#         ],
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'PARSER_CLASS': 'redis.connection.HiredisParser',
#         },
#         'TIMEOUT': 24 * 60 * 60,
#         'TIMEOUT_1H': 60 * 60,
#         'VERSION': CACHE_VERSION
#     }
# }
# DJANGO_REDIS_IGNORE_EXCEPTIONS = True
# DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
# DJANGO_REDIS_LOGGER = '%s.%s' % (LOG_ROOT, __name__)
if TESTING:
    # use dummy when running tests.
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
# Force enable the toolbar in docker container
def show_toolbar(request):
    return TESTING is False
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'sample.settings.localhost.show_toolbar',
}
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
########## END TOOLBAR CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi_localhost.application' % SITE_NAME
########## END WSGI CONFIGURATION


########## CORS CONFIGURATION
# See: https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True
########## END CORS CONFIGURATION

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'sample': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'subdomains': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

# sample CUSTOM DEFINE
AWS_REGION_NAME = 'ap-northeast-1'

# Enable weaker but faster algorithms
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
