from django import template
from django.conf import settings

from django_tables2.utils import AttributeDict

register = template.Library()


@register.simple_tag
def render_attrs(attrs, **kwargs):
    ret = AttributeDict(kwargs)

    if attrs is not None:
        ret.update(attrs)

    return ret.as_html()


@register.filter
def table_page_range(page, paginator):
    page_range = getattr(settings, 'DJANGO_TABLES2_PAGE_RANGE', 10)

    num_pages = paginator.num_pages
    if num_pages <= page_range:
        return range(1, num_pages + 1)

    range_start = page.number - int(page_range / 2)
    if range_start < 1:
        range_start = 1
    range_end = range_start + page_range
    if range_end >= num_pages:
        range_start = num_pages - page_range + 1
        range_end = num_pages + 1

    ret = range(range_start, range_end)
    if 1 not in ret:
        ret = [1, '...'] + list(ret)[2:]
    if num_pages not in ret:
        ret = list(ret)[:-2] + ['...', num_pages]
    return ret
