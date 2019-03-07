from datetime import datetime, date, time

from dateutil import parser
from django import template
from django.utils import six


register = template.Library()


@register.filter(name='get')
def get(d, k):
    return d.get(k, None)


@register.filter('as_dt')
def as_dt(value):
    """
    Converts a str to datetime obj or returns datetime
    """
    if isinstance(value, six.string_types):
        return parser.parse(value)

    if not value or isinstance(value, (datetime, date, time)):
        return value

    raise ValueError('%s is not datetime' % value)
