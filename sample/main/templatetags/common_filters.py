import json

import pytz
from dateutil import parser
from dateutil.parser import parse
from django import template
from django.utils.safestring import mark_safe
from django.utils.six import moves
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from utils.dateutils import get_utc_time, get_jst_time

register = template.Library()
UNSET = object()


@register.filter(name='has_perm')
def has_perm(user, perm):
    return user is not None and user.is_authenticated and (
        user.is_superuser or user.has_perm(perm))


@register.simple_tag(takes_context=True)
def subdomain_url(context, view, subdomain=UNSET, scheme=UNSET, *args, **kwargs):
    request = context.get('request')

    if subdomain is UNSET:
        if request is not None:
            subdomain = getattr(request, 'subdomain', None)
        else:
            subdomain = None
    elif subdomain is '':
        subdomain = None
    if scheme is UNSET:
        scheme = None

    return reverse(view, subdomain=subdomain, scheme=scheme, args=args, kwargs=kwargs, request=request)


@register.filter(name='get_localtime')
def get_localtime(dt):
    if dt:
        dt = get_jst_time(dt)
    return dt


@register.filter(name='str_to_date')
def str_to_date(text):
    # pytz.timezone('Asia/Tokyo') returns 0919 instead of 0900 somehow.
    return parser.parse(text).astimezone(pytz.FixedOffset(9 * 60)).replace(tzinfo=None)


@register.filter(name='get_host')
def get_host(url):
    try:
        urls = moves.urllib_parse.urlparse(url) if url is not None else ''
    except ValueError:
        urls = ''
    if urls:
        return urls.netloc
    else:
        return ''


@register.filter(name='str_replace')
def str_replace(text, replace_text):
    return text % replace_text


@register.filter(name='remove_linebreaks')
def remove_linebreaks(value):
    return value.replace('\r', '').replace('\n', '')


@register.filter(name='remove_dot')
def remove_dot(value):
    return str(round(value, 1)).replace('.', '')


@register.filter(name='remove_dot_str')
def remove_dot_str(value):
    return str(round(float(value), 1)).replace('.', '')


@register.filter(name='division')
def division(numerator, denominator, digits=2):
    if int(numerator):
        return round(float(numerator) / float(denominator), int(digits))
    return 0


@register.filter
def get_days_to_today(dt):
    if dt:
        date_delta = get_utc_time().date() - dt.date()
        return date_delta.days
    return 0


@register.filter
def parse_date(string):
    return parse(string)


@register.simple_tag
def clear_filter_button(cl, *param_names):
    return mark_safe(
        "<a href='{}'>⨉{}</a>".format(
            cl.get_query_string({}, param_names),
            _("Remove")
        )
    )


# Escape content for use in json
@register.simple_tag()
def escape_json(content):
    if content:
        try:
            escaped_content = json.dumps(content)
            return mark_safe(escaped_content[1:-1])
        except:
            pass

    return ""
