# -*- coding:utf-8 -*-
import datetime
import enum
import logging

import boto3
import django_mobile
from django.conf import settings
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.cache import get_cache_key
from redis import ConnectionPool, StrictRedis

from cache.constants import RedisDatabaseEnum
from utils.dateutils import get_jst_time

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))

CACHE_BACKEND = getattr(settings, 'CACHES').get('default').get('BACKEND', '')


class CacheWrapper(object):
    @staticmethod
    def get_cache(name):
        client = None
        try:
            if CACHE_BACKEND == 'django_redis.cache.RedisCache':
                client = cache.client.get_client()
                return cache.get(name, client=client)
            else:
                return cache.get(name)
        except Exception as e:
            if CACHE_BACKEND == 'django_redis.cache.RedisCache':
                server = cache.client.get_server(client=client)
                logger.error('Error in server %s: %s' % (server, e))
            else:
                logger.error(e)

    @staticmethod
    def set_cache(name, value, sec=3600):
        try:
            cache.set(name, value, sec)
        except Exception as e:
            # if you want to copy below, Make a wrapper class.
            # Don't copy and paste
            if getattr(value, 'query', None):
                logger.error(e, extra={
                    'data': {
                        'sql.model': value,
                        'sql.query': str(value.query),
                        'sql.records': value.count()
                    }
                })
            else:
                logger.error(e, extra={
                    'data': {'value': value}
                })

    @staticmethod
    def delete_cache(name):
        try:
            cache.delete(name)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def delete_pagination_template_cache(fragment_name, vary_on=None):
        if vary_on is None:
            vary_on = []

        # Delete null string pagination cache if it exists
        page = ''
        vary_on.append(page)
        template_cache_key = make_template_fragment_key(fragment_name, vary_on)
        cache.delete(template_cache_key)

        # Delete pagination cache
        page = 1
        while page <= 30:
            vary_on[-1] = page
            template_cache_key = make_template_fragment_key(fragment_name, vary_on)
            cache.delete(template_cache_key)
            page += 1

    @staticmethod
    def delete_page_cache(request):
        # backup request's variables
        backup_path = request.path
        backup_flavour = request.META.get('HTTP_X_FLAVOUR')
        # replace URL
        request.path = request.path.replace('preview/', '')
        # clear cache for every flavours of the page.
        # Be aware that this workaround doesn't support i18n or l10n at the moment.
        # cache.delete() is None-proof.
        for flavour in settings.FLAVOURS:
            # set X-FLAVOUR header
            # noinspection PyProtectedMember
            django_mobile._set_request_header(request, flavour)
            cache.delete(get_cache_key(request, settings.CACHE_MIDDLEWARE_KEY_PREFIX))
        # restore variables from backup
        request.path = backup_path
        request.META['HTTP_X_FLAVOUR'] = backup_flavour


@enum.unique
class CountObject(enum.Enum):
    shop = 'shop'
    cast = 'cast'


@enum.unique
class CountAction(enum.Enum):
    pageview = 'pageview'


class RedisClient(object):
    # write-only pool
    write_pool = None

    def __init__(self):
        # self.write_pool will reference a different object once its value is set.
        # See http://stackoverflow.com/a/25577642
        if RedisClient.write_pool is None:
            RedisClient.write_pool = ConnectionPool(
                host=getattr(settings, 'REDIS_PRIMARY_ENDPOINT'), **self._connection_info())

    @staticmethod
    def _connection_info(db=int(RedisDatabaseEnum.counter)):
        """
        :param db db identifier.
        :return: dict data required for redis.
        """
        return {
            'port': 6379,
            'db': db,
            'decode_responses': True,
        }

    @staticmethod
    def _key(obj, action, day_offset=0):
        """
        :param obj: one of CountObject values
        :param action: one of CountAction values
        :param day_offset: 1 for getting the key of yesterday.
        :return: key string    ex. 'spot-pageview-20170110'
        """
        return '{}-{}-{}'.format(
            obj.value, action.value, get_jst_time(delta=-datetime.timedelta(
                days=day_offset)).strftime('%Y%m%d'))

    @staticmethod
    def _replica_host():
        """
        :return: Only first replica found in the response or Primary Endpoint in case of errors.
        """
        client = boto3.client('elasticache', region_name=settings.AWS_REGION_NAME,
                              aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        try:
            result = client.describe_replication_groups(ReplicationGroupId=settings.REDIS_CLUSTER)
            for m in result.get('ReplicationGroups')[0].get('NodeGroups')[0].get('NodeGroupMembers'):
                if m.get('CurrentRole') == 'replica':
                    return m.get('ReadEndpoint').get('Address')
        except Exception as e:
            # couldn't find replica entry in the result so fallback to the primary endpoint
            # or describe_replication_groups() threw an exception.
            logger.error(e)
        # use fallback endpoint.
        return getattr(settings, 'REDIS_PRIMARY_ENDPOINT')

    def count_up(self, obj, action, value):
        """
        :param obj: one of CountObject values
        :param action: one of CountAction values
        :param value: object id
        """

        key = self._key(obj, action)
        try:
            r = StrictRedis(connection_pool=RedisClient.write_pool)
            r.zincrby(key, value)
        except Exception as e:
            # output error and let it continue.
            logger.error(e)
