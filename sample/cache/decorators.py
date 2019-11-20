import logging

from django.conf import settings
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args

from cache.middleware import CacheFlavourRequestMiddleware, CacheFlavourResponseMiddleware, ResilientCacheMiddleware

__all__ = ('cache_page', 'vary_on_flavour_request', 'vary_on_flavour_response')

vary_on_flavour_request = decorator_from_middleware(CacheFlavourRequestMiddleware)
vary_on_flavour_response = decorator_from_middleware(CacheFlavourResponseMiddleware)

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


def cache_page(*args, **kwargs):
    def flavoured_decorator(func):
        return vary_on_flavour_request(_cache_page(*args, **kwargs)(vary_on_flavour_response(func)))

    return flavoured_decorator


def _cache_page(*args, **kwargs):
    """
    Copied almost everything from the original except replacing the middleware.
    """
    # We also add some asserts to give better error messages in case people are
    # using other ways to call cache_page that no longer work.
    if len(args) != 1 or callable(args[0]):
        raise TypeError("cache_page has a single mandatory positional argument: timeout")
    cache_timeout = args[0]
    cache_alias = kwargs.pop('cache', None)
    key_prefix = kwargs.pop('key_prefix', None)
    if kwargs:
        raise TypeError("cache_page has two optional keyword arguments: cache and key_prefix")

    return decorator_from_middleware_with_args(ResilientCacheMiddleware)(cache_timeout=cache_timeout,
                                                                         cache_alias=cache_alias,
                                                                         key_prefix=key_prefix)