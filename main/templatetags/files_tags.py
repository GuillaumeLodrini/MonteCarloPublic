import os

from django import template
from django.conf import settings


register = template.Library()


@register.filter
def read_svg(path):
    content = ''

    with open(os.path.join(settings.STATIC_ROOT, path)) as f:
        content = f.read()

    return content
