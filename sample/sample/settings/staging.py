# -*- coding:utf-8 -*-

import re
"""Production settings and globals."""
from .base import *
# For OpsWorks
from .settings_base_credential import *
from .settings_staging_credential import *

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['staging.sample.jp', 'staging-api.sample.jp', 'staging-managing.sample.jp']
########## END HOST CONFIGURATION


########## URL CONFIGURATION
# A dictionary of urlconf module paths, keyed by their subdomain.

SUBDOMAIN_API = 'staging-api-u2o82igj'
SUBDOMAIN_MANAGING = 'staging-managing'
SUBDOMAIN_URLCONFS = {
    None: '%s.urls.frontend' % SITE_NAME,  # no subdomain, e.g. ``sample.jp``
    'staging': '%s.urls.frontend' % SITE_NAME,
    SUBDOMAIN_API: '%s.urls.api' % SITE_NAME,
    SUBDOMAIN_MANAGING: '%s.urls.managing' % SITE_NAME,
}
########## END URL CONFIGURATION


########## CACHE CONFIGURATION
# RedisClient settings
REDIS_CLUSTER = 'sample-staging'
REDIS_PRIMARY_ENDPOINT = 'sample-staging.twv8q6.ng.0001.apne1.cache.amazonaws.com'
# Django Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            # Primary floating domain name.
            'redis://{}:6379/0'.format(REDIS_PRIMARY_ENDPOINT),
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'cache.wrapper.RedisServerClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'TIMEOUT': 24 * 60 * 60,
        'TIMEOUT_1H': 60 * 60,
        'VERSION': CACHE_VERSION
    }
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
DJANGO_REDIS_LOGGER = '%s.%s' % (LOG_ROOT, __name__)
########## END CACHE CONFIGURATION


# # ######### DEBUG CONFIGURATION
# # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
# DEBUG = True
# TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
# ########## END DEBUG CONFIGURATION
#
#
# ########## TOOLBAR CONFIGURATION
# # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
# INSTALLED_APPS += (
#     'debug_toolbar',
# )
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# # Force enable the toolbar in docker container
# def show_toolbar(request):
#     return TESTING is False and request.user.is_superuser
# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': 'sample.settings.staging.show_toolbar',
# }
# # See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
# MIDDLEWARE += (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
# HIDDEN_SETTINGS = re.compile('API|TOKEN|KEY|SECRET|PASS|SIGNATURE|RECAPTCHA|CREDENTIAL', flags=re.IGNORECASE)
# ########## END TOOLBAR CONFIGURATION


########## DYNAMO DB CONFIGRATION
SESSION_ENGINE = 'dynamodb2_sessions.backends.dynamodb'
DYNAMODB_SESSIONS_TABLE_NAME = 'sample-staging-sessions'
AWS_REGION_NAME = 'ap-northeast-1'
########## END DYNAMO DB CONFIGRATION


########## STATIC FILES CONFIGURATION
AWS_STORAGE_BUCKET_NAME = 'sample-dev'
S3_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'sample.storage.S3HashedFilesStorage'
AWS_LOCATION = 'static'  # collectstatic Upload時のみに利用される
STATIC_URL = 'https://{}/static/'.format(CDN_DOMAIN)
AWS_S3_CUSTOM_DOMAIN = CDN_DOMAIN
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Cache-Control': 'max-age=31536000',
}
DEFAULT_MOVIE_ENVIRONMENT = 'staging'  # specifies path within bucket to upload files too
SNS_TOPIC_MOVIE_UPLOAD_COMPLETE_ARN = 'arn:aws:sns:ap-northeast-1:523323460302:sample-transcoder-staging'
########## END STATIC FILES CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi_staging.application' % SITE_NAME
########## END WSGI CONFIGURATION

# Modify Logging
LOGGING['handlers']['fluent_django']['tag'] = 'sample.staging/django'


# CELERY
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'ap-northeast-1',
    'visibility_timeout': 3600,
    'polling_interval': 1,
    'queue_name_prefix': 'sample-staging-',
}


CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?://)?([\w\-]+\.)?(sample)\.jp$',
    r'^(https?://)?localhost(:[0-9]+)?$',
)
