from datetime import datetime

from django import template

register = template.Library()


@register.simple_tag
def multiply(first, second, *args, **kwargs):
    return first * second



