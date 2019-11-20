# -*- coding:utf-8 -*-
from django_mobile import set_flavour
from django_mobile.conf import settings
from django_mobile.middleware import MobileDetectionMiddleware


class ExtendMobileDetectionMiddleware(MobileDetectionMiddleware):
    """
    django admin のページを開く際、django_mobile の flavour によって、
    template の読み込み dir が変更されるため、admin(managing)用の flavour を加えてあげる
    """
    def process_request(self, request):
        super(ExtendMobileDetectionMiddleware, self).process_request(request)
        if request.subdomain == settings.SUBDOMAIN_API:
            set_flavour(settings.FLAVOURS[3], request)
        if request.subdomain == settings.SUBDOMAIN_MANAGING:
            set_flavour(settings.FLAVOURS[2], request)
