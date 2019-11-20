import copy

from django.conf import settings


def use_locmemcache():
    caches = copy.deepcopy(settings.CACHES)
    caches['default']['BACKEND'] = 'django.core.cache.backends.locmem.LocMemCache'
    return {'CACHES': caches}


def use_redis_general_cache():
    return {
        'CACHES': {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': [
                    'redis://{}:6379/0'.format(getattr(settings, 'REDIS_PRIMARY_ENDPOINT')),
                ],
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'PARSER_CLASS': 'redis.connection.HiredisParser',
                },
                'TIMEOUT': 24 * 60 * 60,
                'TIMEOUT_1H': 60 * 60,
                'VERSION': getattr(settings, 'CACHE_VERSION'),
            }
        }
    }
