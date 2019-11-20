import hashlib
import logging

from django.conf import settings
from django.utils.cache import patch_cache_control
from django.utils.encoding import smart_bytes

from cache.wrapper import CacheWrapper

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


class PublicApiCacheMixin(object):
    """ cache mixin for API.
    """
    CACHE_TIMEOUT = 1800  # 30 minutes by default.
    CACHE_KEY_PREFIX = 'sample_api'
    CACHE_HIT_BOOLEAN_NAME = 'sample_api_cache_hit'  # use this name as field name of dynamic request object.
    DISABLE_CACHE_CONTROL = False  # overwrite this to disable cache-control:no-cache header.

    def list(self, request, *args, **kwargs):
        # see if parent has list().
        if hasattr(super(PublicApiCacheMixin, self), 'list'):
            return self._cache('list', request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # see if parent has retrieve().
        if hasattr(super(PublicApiCacheMixin, self), 'retrieve'):
            return self._cache('retrieve', request, *args, **kwargs)

    def _cache(self, method, request, *args, **kwargs):
        """ called by list or retrieve.
        :param method: string "list" or "retrieve"
        :param request:
        :param args:
        :param kwargs:
        :return: response
        """
        if not self._is_cacheable():
            # cache is disabled so the response doesn't need to be cached.
            return getattr(super(PublicApiCacheMixin, self), method)(request, *args, **kwargs)
        cache_key = self._make_cache_key(request)
        # try retrieving cache
        response = CacheWrapper.get_cache(cache_key)
        if response is None or self._is_clearing_cache():
            # call parent's list() or retrieve().
            response = getattr(super(PublicApiCacheMixin, self), method)(request, *args, **kwargs)
            # set cache
            # this code was inspired by https://docs.djangoproject.com/en/1.7/_modules/django/middleware/cache/
            response.add_post_render_callback(
                lambda r: CacheWrapper.set_cache(cache_key, r, self.CACHE_TIMEOUT)
            )
            setattr(request, self.CACHE_HIT_BOOLEAN_NAME, False)
        else:
            setattr(request, self.CACHE_HIT_BOOLEAN_NAME, True)
        # set cache-control header to enable client-side cache.
        # you don't need to worry about curator API since requests with version < 1 won't reach here
        # (excluded by _is_cacheable() in the beginning of this function).
        patch_cache_control(response, max_age=self.CACHE_TIMEOUT)
        return response

    @classmethod
    def _make_cache_key(cls, request, url=None):
        """ make cache key.
        this method must be class method since it's called from other class method.

        :return: key string ex. sample_api:47bce5c74f589f4867dbd57e9ca9f808
        """
        absolute_uri = url if url is not None else request.build_absolute_uri()
        hashed_parameters = hashlib.md5(smart_bytes(
            ','.join([str(request.version), absolute_uri])
        )).hexdigest()
        return ':'.join([cls.CACHE_KEY_PREFIX, hashed_parameters])

    def _is_cacheable(self):
        """ cache will be disable if one of these conditions is met.
        - CACHE_TIMEOUT = None
        - request.version is less than 1

        :return: bool
        """
        # noinspection PyUnresolvedReferences
        return self.CACHE_TIMEOUT is not None and self.request.version >= 1

    def _is_clearing_cache(self):
        """
        cache will be cleared if the HTTP header below is set.

        Cache-Control: no-cache

        Subclasses can control this by overwriting DISABLE_CACHE_CONTROL class variable.

        :return: True if the header has no-cache param, or False if there's no no-cache param in the header of DISABLE_CACHE_CONTROL is set to True.
        """
        # Force returning False if the class set this flag to True.
        # we don't need to check request.version since the check is done in _is_cacheable() beforehand.
        if self.DISABLE_CACHE_CONTROL:
            return False
        # noinspection PyUnresolvedReferences
        return 'no-cache' in self.request.META.get('HTTP_CACHE_CONTROL', '').lower()

    @classmethod
    def invalidate_cache(cls, request, url):
        CacheWrapper.delete_cache(cls._make_cache_key(request, url=url))


class PrivateApiCacheMixin(PublicApiCacheMixin):
    """ User specific version of PublicApiCacheMixin.
    """

    @classmethod
    def _make_cache_key(cls, request, url=None):
        """
        :return: key string ex. sample_api:12345:47bce5c74f589f4867dbd57e9ca9f808
        """
        absolute_uri = url if url is not None else request.build_absolute_uri()
        user_id = request.user.id if request.user.is_authenticated else 0
        hashed_parameters = hashlib.md5(smart_bytes(
            ','.join([str(request.version), absolute_uri])
        )).hexdigest()
        return ':'.join([cls.CACHE_KEY_PREFIX, str(user_id), hashed_parameters])


class HeaderInclusivePublicApiCacheMixin(PublicApiCacheMixin):
    """
    PublicApiCacheMixin derivative which takes into account a specified request headers as well as url
    """
    # classes inheriting from this mixin should override this value with the specific headers to cache against
    CACHE_HEADERS = None
    CACHE_TIMEOUT = 21600  # 6 hours by default.

    def _cache(self, method, request, *args, **kwargs):
        """ called by list or retrieve.
        :param method: string "list" or "retrieve"
        :param request:
        :param args:
        :param kwargs:
        :return: response
        """
        if not self._is_cacheable():
            # cache is disabled so the response doesn't need to be cached.
            return getattr(super(PublicApiCacheMixin, self), method)(request, *args, **kwargs)
        cache_key = self._make_cache_key(request)
        # try retrieving cache
        response = CacheWrapper.get_cache(cache_key)
        if response is None or self._is_clearing_cache():
            # call parent's list() or retrieve().
            response = getattr(super(PublicApiCacheMixin, self), method)(request, *args, **kwargs)
            # set cache
            # this code was inspired by https://docs.djangoproject.com/en/1.7/_modules/django/middleware/cache/
            response.add_post_render_callback(
                lambda r: CacheWrapper.set_cache(cache_key, r, self.CACHE_TIMEOUT)
            )
            setattr(request, self.CACHE_HIT_BOOLEAN_NAME, False)
        else:
            setattr(request, self.CACHE_HIT_BOOLEAN_NAME, True)
        # set cache-control header to enable client-side cache.
        # you don't need to worry about curator API since requests with version < 1 won't reach here
        # (excluded by _is_cacheable() in the beginning of this function).
        patch_cache_control(response, max_age=self.CACHE_TIMEOUT)
        return response

    @classmethod
    def _make_cache_key(cls, request, url=None):
        """
        :return: key string ex. sample_api:47bce5c74f589f4867dbd57e9ca9f808
        """
        absolute_uri = url if url is not None else request.build_absolute_uri()
        header_values = []
        for header_name in cls.CACHE_HEADERS:
            value = request.META.get(header_name, '0')
            header_values.append(str(value))
        header_values = header_values or ['']
        hashed_parameters = hashlib.md5(smart_bytes(
            ','.join([str(request.version), absolute_uri] + header_values)
        )).hexdigest()
        return ':'.join([cls.CACHE_KEY_PREFIX, hashed_parameters])
