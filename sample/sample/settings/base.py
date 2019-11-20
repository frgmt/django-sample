# -*- coding:utf-8 -*-
"""Common settings and globals."""
import sys
from os.path import abspath, basename, dirname, join, normpath

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)
# Site name:
SITE_NAME = basename(DJANGO_ROOT)
# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
sys.path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION

########## CACHE VERSIONING
# Increase this value when you create a new migration file.
CACHE_VERSION = 1
########## END CACHE VERSIONING

########## SECURE SETTING
# Using is_secure behind nginx
# See: https://docs.djangoproject.com/en/1.7/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

########## SESSION CONFIGRATION
CSRF_COOKIE_DOMAIN = '.sample.jp'
CSRF_TRUSTED_ORIGINS = ['.sample.jp',]
SESSION_COOKIE_DOMAIN = '.sample.jp'
SESSION_COOKIE_AGE = 2419200
# SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
########## END DEBUG CONFIGURATION

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False
########## END DEBUG CONFIGURATION

SERVER_EMAIL = 'info@sample.jp'
SUPPORT_EMAIL = 'support@sample.jp'
DEFAULT_FROM_EMAIL = SERVER_EMAIL
GENERAL_EMAIL = 'sample <mail@sample.jp>'

EMAILS_PER_SECOND = 80

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Administrator', 'n.anahara@fragment.co.jp'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ja'
# for intcomma
NUMBER_GROUPING = 3

LANGUAGES = (
    ('ja', 'Japanese'),
)

LOCALE_PATHS = ['%s/locale/' % SITE_ROOT]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## LOGIN CONFIGURATION
LOGIN_URL = '/login/'
########## END LOGIN CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
# collect static する場合は必須。ただし、s3boto を利用する場合はデフォルト値で良いのでコメントアウトしておく
# STATIC_ROOT = normpath(join(SITE_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
CDN_DOMAIN = 'staging-static.sample.jp'
CDN_DOMAIN_MOVIE = 'video.sample.jp'
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = r"^z(!&%ys=q*6&!7ibdvscl&)wag*(l1cgbt(u#!l-^vsyj7#l2"
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
########## END SITE CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(SITE_ROOT, 'templates')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django_mobile.context_processors.flavour',
                'sample.context_processors.global_settings',
            ],
            'loaders': [
                'django_mobile.loader.Loader',
                ('django.template.loaders.cached.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                )),
            ],
            'debug': DEBUG
        },
    },
]
# https://github.com/gregmuellegger/django-mobile/issues/72
TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']
########## END TEMPLATE CONFIGURATION


########## MOBILE CONFIGURATION
FLAVOURS = ('pc', 'sp', 'managing', 'api')
DEFAULT_PC_FLAVOUR = 'pc'
DEFAULT_MOBILE_FLAVOUR = 'sp'
DEFAULT_ADMIN_FLAVOUR = 'managing'
########## END MOBILE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = (
    ## These Middleware should be defined before CommonMiddleware
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'sample.middleware.https.UrlRedirectMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'sample.middleware.https.CorsOverHttpsMiddleware',
    ##
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'sample.middleware.flavour.ExtendMobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'linaro_django_pagination.middleware.PaginationMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls.frontend' % SITE_NAME

# A dictionary of urlconf module paths, keyed by their subdomain.
SUBDOMAIN_API = 'api'
SUBDOMAIN_MANAGING = 'managing'
SUBDOMAIN_URLCONFS = {
    None: '%s.urls.frontend' % SITE_NAME,  # no subdomain, e.g. ``sample.jp``
    'www': '%s.urls.frontend' % SITE_NAME,
    SUBDOMAIN_API: '%s.urls.api' % SITE_NAME,
    SUBDOMAIN_MANAGING: '%s.urls.managing' % SITE_NAME,
    # Consider modifying CspHeaderMiddleware if you happen to alter this list because the middleware depends on it.
}
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',
    # Admin panel and documentation:
    'django.contrib.admin',
    # GeoDjango
    'django.contrib.gis',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'main',
    'users',
    'cache',
    'sample',
    'utils',
)

THIRD_PARTY_APPS = (
    'linaro_django_pagination',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'corsheaders',
    'subdomains',
    'django_filters',
    'rangefilter',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
########## END APP CONFIGURATION

# auth model
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'users.backends.FacebookBackend',  # facebook login
    'users.backends.TwitterBackend',  # twitter login
    'users.backends.InstagramBackend',  # instagram login
    'users.backends.LineBackend',  # line login
    'users.backends.MailLoginBackend',  # mail and password
    # ModelBackend is the slowest therefore is the last of the list.
    'django.contrib.auth.backends.ModelBackend',  # user and password
)

# Avoid writing too much data to the session storage by using CookieStorage.
# https://docs.djangoproject.com/en/2.0/ref/contrib/messages/
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'fluent_django': {
            'level': 'INFO',
            'class': 'log.handlers.FluentDjangoHandler',
            'tag': 'sample.testing/django',
            'host': 'localhost',
            'port': 24224,
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['sentry'],
            # stop sending error reports.
            # See http://stackoverflow.com/questions/18220519/how-to-disable-djangos-invalid-http-host-error
            'level': 'CRITICAL',
            'propagate': False,
        },
        'celery': {
            'handlers': ['fluent_django', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
        'sample': {
            'handlers': ['fluent_django', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

# defining root of the logging hierarchy. used by getLogger().
LOG_ROOT = 'sample'
LOG_STATS_ROOT = 'sample.stats'
########## END LOGGING CONFIGURATION

# Raven/Sentry
SENTRY_AUTO_LOG_STACKS = True
#################


# AWS
USE_AMAZON_S3 = True
DEFAULT_BUCKET = 'sample-dev'
DEFAULT_MOVIE_BUCKET = 'sample-transcoder'
DEFAULT_MOVIE_ENVIRONMENT = 'development'  # specifies path within bucket
DEFAULT_BACKUP_BUCKET = 'sample-backup'
DEFAULT_BACKUP_ENVIRONMENT = 'development'  # specifies path within bucket
UNCONVERTED_MOVIE_PREFIX = 'input'
CONVERTED_MOVIE_PREFIX = 'output'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:523323460302:sample-ses'
SNS_TOPIC_MOVIE_UPLOAD_COMPLETE_ARN = 'arn:aws:sns:ap-northeast-1:523323460302:sample-transcoder-development'

# designate bcrypt as the hashing algorithm to store passwords.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# rest-framework specific settings.
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'utils.authentication.AppendEffectiveUserTokenAuthentication',
    ),
    # Permission
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Throttling
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'edit': '12/minute',
    },
    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'sample.paginations.StandardPageNumberPagination',
    # error handler
    'EXCEPTION_HANDLER': 'utils.exception_handlers.custom_exception_handler',
    # Versioning
    'DEFAULT_VERSIONING_CLASS': 'utils.versioning.NumericAcceptHeaderVersioning',
    'DEFAULT_VERSION': '1.0',
    'ALLOWED_VERSIONS': ('0.1', '1.0'),
    'VERSION_PARAMETER': 'version',
    # enable django-rest_swagger(CUSTOM)
    'ENABLE_DOCS': True,
}

########## CORS CONFIGURATION for API
# See: https://github.com/ottoyiu/django-cors-headers/
CORS_ORIGIN_REGEX_WHITELIST = (
    r'^(https?://)?([\w\-]+\.)?sample\.jp$',
)
CORS_ALLOW_HEADERS = ('x-requested-with', 'content-type', 'accept', 'origin', 'authorization',
                      'x-csrftoken', 'cache-control')
CORS_ALLOW_CREDENTIALS = True
########## END CORS CONFIGURATION


########## DJANGO-PAGINATION
# see https://pypi.python.org/pypi/django-pagination
PAGINATION_INVALID_PAGE_RAISES_404 = True
PAGINATION_DEFAULT_WINDOW = 2
PAGINATION_DEFAULT_PAGINATION = 30
# There's a bug in linaro_django_pagination.templatetags.pagination_tags.paginate. The request context is forgotten to
# be included in the new_context. Disabling the default value works around the issue.
PAGINATION_DISABLE_LINK_FOR_FIRST_PAGE = False
########## END DJANGO-PAGINATION

# testing detection
TESTING = sys.argv[1:2] == ['test']

# sample CUSTOM DEFINE
SYSTEM_USER_ID = 1
DEFAULT_MAX_FILE_SIZE = 10485760  # 10MB
ALLOW_IMAGE_MIME_TYPE = ('image/gif', 'image/jpeg', 'image/png')
ALLOW_MOVIE_MIME_TYPE = ('video/mp4', 'video/quicktime')
FAVICON_PATH = '%simg/common/favicon.ico' % STATIC_URL
REDIRECT_HTTPS_DISABLE = False  # Use only in development env or check server alive. used in sample/middleware
# dynamodb2_sessions common setting. ref: #355
DYNAMODB_SESSIONS_ALWAYS_CONSISTENT = True
# redis (default)
REDIS_CLUSTER = 'sample-staging'
REDIS_PRIMARY_ENDPOINT = 'localhost'
