# -*- coding: utf-8 -*-

"""Production settings and globals."""
from .base import *
# For OpsWorks
try:
    from .settings_base_credential import *
    from .settings_production_credential import *
except ImportError:
    # For Containers
    # Let it raise ImportError should it fail.
    from .container_credential_loader import *


########## SCHEME CONFIGURATION
DEFAULT_URL_SCHEME = 'https'
########## END SCHEME CONFIGURATION


########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['sample.jp', 'www.sample.jp', 'api.sample.jp', 'managing.sample.jp']
########## END HOST CONFIGURATION


########## CACHE CONFIGURATION
# RedisClient settings
REDIS_CLUSTER = 'sample-pro'
REDIS_PRIMARY_ENDPOINT = 'sample-pro.twv8q6.ng.0001.apne1.cache.amazonaws.com'
# Django Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            # Primary floating domain name.
            'redis://{}:6379/0'.format(REDIS_PRIMARY_ENDPOINT),
            # Replicas (Swap the replica in case of fail-over)
            # 'redis://sample-pro-002.twv8q6.0001.apne1.cache.amazonaws.com:6379/0',
            'redis://sample-pro-001.twv8q6.0001.apne1.cache.amazonaws.com:6379/0',
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


########## DYNAMO DB CONFIGRATION
SESSION_ENGINE = 'dynamodb2_sessions.backends.dynamodb'
DYNAMODB_SESSIONS_TABLE_NAME = 'sample-sessions'
AWS_REGION_NAME = 'ap-northeast-1'
########## END DYNAMO DB CONFIGRATION


########## STATIC FILES CONFIGURATION
AWS_STORAGE_BUCKET_NAME = 'sample'
S3_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'sample.storage.S3HashedFilesStorage'
AWS_LOCATION = 'static'  # collectstatic Upload時のみに利用される
CDN_DOMAIN = 'static.sample.jp'
AWS_S3_CUSTOM_DOMAIN = CDN_DOMAIN
STATIC_URL = 'https://{}/static/'.format(CDN_DOMAIN)
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Cache-Control': 'max-age=31536000',
}
########## END STATIC FILES CONFIGURATION

########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi_production.application' % SITE_NAME
########## END WSGI CONFIGURATION

# AWS
USE_AMAZON_S3 = True
DEFAULT_BUCKET = 'sample'
DEFAULT_MOVIE_ENVIRONMENT = 'production'  # specifies path within bucket to upload files too
DEFAULT_BACKUP_ENVIRONMENT = 'production'  # specifies path within bucket
SNS_TOPIC_MOVIE_UPLOAD_COMPLETE_ARN = 'arn:aws:sns:ap-northeast-1:523323460302:sample-transcoder-production'

# Modify Logging
LOGGING['handlers']['fluent_django']['tag'] = 'sample.production/django'

# sample CUSTOM DEFINE
DYNAMODB_PREFIX = 'sample-'
DYNAMODB_PAGE_VIEWS_ACCESS_LOG_TABLE_NAME = '{0}page-views-access-log'.format(DYNAMODB_PREFIX)
DYNAMODB_PAGE_VIEWS_TABLE_NAME = '{0}page-views'.format(DYNAMODB_PREFIX)
DYNAMODB_IMAGE_META_TABLE_NAME = '{0}image-meta'.format(DYNAMODB_PREFIX)
DYNAMODB_EXTERNAL_LINK_TABLE_NAME = '{0}external-link'.format(DYNAMODB_PREFIX)
DYNAMODB_SUPPLIER_SPOT_CONTENTS_TABLE_NAME = '{0}supplier-spot-contents'.format(DYNAMODB_PREFIX)
DYNAMODB_PAID_IMAGE_USAGE_BY_USER_TABLE_NAME = '{0}paid-image-usage-by-user'.format(DYNAMODB_PREFIX)
DYNAMODB_SPOT_IMAGE_FILE_TABLE_NAME = '{0}spot-image-file-data'.format(DYNAMODB_PREFIX)
DYNAMODB_SPOT_LANG_DATA_TABLE_NAME = '{0}spot-lang-data'.format(DYNAMODB_PREFIX)
DYNAMODB_JACK_AD_METRIC_TABLE_NAME = '{0}jack-ad-metric'.format(DYNAMODB_PREFIX)
ENCRYPTED_FIELDS_KEYDIR = normpath(join(dirname(abspath(__file__)), 'fieldkeys/production'))

#
# Override DRF settings.
#
# swagger
REST_FRAMEWORK['ENABLE_DOCS'] = False
# throttle
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = (
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle'
)
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '60/minute',
    'user': '4000/hour'
}
# disable browsable api
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ('rest_framework.renderers.JSONRenderer', )

