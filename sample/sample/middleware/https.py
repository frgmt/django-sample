# -*- coding:utf-8 -*-
import logging
import re

from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.utils import six
from django.utils.deprecation import MiddlewareMixin
from django.utils.six import moves

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))


# noinspection PyMethodMayBeStatic
class UrlRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip the rest of the process on localhost.
        if settings.REDIRECT_HTTPS_DISABLE:
            settings.CSRF_COOKIE_SECURE = False
            settings.SESSION_COOKIE_SECURE = False
            return None

        # URL: http(s)://www.sample.jp/*
        if request.subdomain == 'www':
            url = request.site.domain + request.get_full_path()
            return HttpResponsePermanentRedirect('https://%s' % url)

        # the protocol isn't secure OR ELB didn't use https
        if not request.is_secure():
            url = request.META.get('HTTP_HOST', request.site.domain) + request.get_full_path()
            return HttpResponsePermanentRedirect('https://%s' % url)

        return None


class CorsOverHttpsMiddleware(MiddlewareMixin):
    """
    CORS + HTTPS 環境で、ドメインが同じであれば、通信を許す。

    HTTPS環境の場合、django.middleware.csrf.CsrfViewMiddleware は
    Referer チェックまで行うため、以下を弾いてしまう。HTTP通信の場合
    そこまでしない。

    Host	api.sample.local
    Origin	https://sample.local
    Referer	https://sample.local/articles/1456/

    * host と Referer の hostnameが異なるため

    詳細は、以下ソースコード参照のこと
      - django.middleware.csrf.CsrfViewMiddleware
      - django.utils.http.same_origin
      - rest_framework.authentication.SessionAuthentication

    なお、リクエストヘッダに HTTP_ORIGIN がある CORS 通信のときだけ、
    本ミドルウェアは有効になる。
    """

    def process_request(self, request):
        # CORS でない場合は、許可しない
        if not request.META.get('HTTP_ORIGIN'):
            return None

        # HOST ヘッダがNONEの場合は、許可しない
        request_host = request.get_host()
        if not request_host:
            return None

        # referer ヘッダがNONEの場合は、許可しない
        referer_url = request.META.get('HTTP_REFERER')
        if not referer_url:
            return None

        if request_host.endswith(request.site.domain):
            referer = moves.urllib_parse.urlparse(referer_url)
            if referer.hostname and isinstance(referer.hostname, six.string_types):
                request.META['HTTP_REFERER'] = referer_url.replace(referer.hostname, request_host)

        return None
