import logging

from django.conf import settings
from django.middleware.cache import CacheMiddleware
from django.utils.cache import patch_vary_headers
# noinspection PyProtectedMember
from django_mobile import get_flavour, _set_request_header


logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


# noinspection PyMethodMayBeStatic
class CacheFlavourRequestMiddleware(object):
    def process_request(self, request):
        _set_request_header(request, get_flavour(request))


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class CacheFlavourResponseMiddleware(object):
    def process_response(self, request, response):
        patch_vary_headers(response, ['X-Flavour'])
        return response


class ResilientCacheMiddleware(CacheMiddleware):
    def process_request(self, request):
        try:
            if not request.user.is_authenticated:
                return super(ResilientCacheMiddleware, self).process_request(request)
        except Exception as e:
            logger.error('detected cache error but continue processing the request.\terror:%s', str(e))

    def process_response(self, request, response):
        try:
            if not request.user.is_authenticated:
                return super(ResilientCacheMiddleware, self).process_response(request, response)
        except Exception as e:
            logger.error('detected cache error but continue processing the response.\terror:%s', str(e))
        # this function must return response.
        return response
