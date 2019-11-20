# -*- coding:utf-8 -*-
import logging

from django.conf import settings
from django.views.generic import TemplateView

from main.contexts import TitleMixin, TemplateUrlMixin

logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))
stats = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_STATS_ROOT'), __name__))


class BaseView(TitleMixin, TemplateUrlMixin, TemplateView):
    pass


class IndexView(BaseView):
    template_name = 'index.html'


class PageNotFoundView(TemplateUrlMixin, TemplateView):
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        response = super(PageNotFoundView, self).get(request, *args, **kwargs)
        response.status_code = 404
        return response
