# -*- coding:utf-8 -*-
import json

from django.conf import settings
from django.templatetags.static import static
from django.utils.translation import ugettext as _

from main.template_urls import TEMPLATE_URL, TEMPLATE_URL_SP


class TitleMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        if 'title' in context:
            context['title'] = '{} | {}'.format(context['title'], _('simple_title'))
        return context


class TemplateUrlMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TemplateUrlMixin, self).get_context_data(**kwargs)

        if self.request.flavour == settings.DEFAULT_MOBILE_FLAVOUR:
            template_urls = TEMPLATE_URL_SP
        else:
            template_urls = TEMPLATE_URL

        if not template_urls.get('converted'):
            template_urls = self._convert_static(template_urls)

        context['template_urls'] = json.dumps(template_urls)

        return context

    def _convert_static(self, urls):
        """
        Converting directly in the module creates problems in the initial import so use this function to call static
        before setting into context data.
        """
        for inner_dict in urls.values():
            for name, url in inner_dict.items():
                inner_dict[name] = static(url)
        urls['converted'] = True

        return urls
