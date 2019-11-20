from __future__ import unicode_literals

import logging

from django.conf import settings
from django.template import Library, TemplateSyntaxError
from django.templatetags.cache import CacheNode


logger = logging.getLogger('%s.%s' % (getattr(settings, 'LOG_ROOT'), __name__))

register = Library()


class CacheNodeWrapper(CacheNode):
    def render(self, context):
        try:
            return super(CacheNodeWrapper, self).render(context)
        except TemplateSyntaxError as e:
            logger.error(e)
            return self.nodelist.render(context)


@register.tag('cache')
def do_cache(parser, token):
    """
    This will cache the contents of a template fragment for a given amount
    of time.

    Usage::

        {% load cache %}
        {% cache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

    This tag also supports varying by a list of arguments::

        {% load cache %}
        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Optionally the cache to use may be specified thus::

        {% cache ....  using="cachename" %}

    Each unique set of arguments will result in a unique cache entry.
    """

    nodelist = parser.parse(('endcache',))
    parser.delete_first_token()
    tokens = token.split_contents()
    if len(tokens) < 3:
        raise TemplateSyntaxError("'%r' tag requires at least 2 arguments." % tokens[0])
    if len(tokens) > 3 and tokens[-1].startswith('using='):
        cache_name = parser.compile_filter(tokens[-1][len('using='):])
        tokens = tokens[:-1]
    else:
        cache_name = None
    return CacheNodeWrapper(
        nodelist,
        parser.compile_filter(tokens[1]),
        tokens[2],  # fragment_name can't be a variable.
        [parser.compile_filter(t) for t in tokens[3:]],
        cache_name,
    )
