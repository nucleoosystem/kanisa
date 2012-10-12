import os
from django import template
from django.conf import settings


register = template.Library()


def __exists(branding_component):
    path = os.path.join(settings.MEDIA_ROOT,
                        'branding',
                        '%s' % branding_component)

    return os.path.exists(path)


def __url(branding_component):
    return 'branding/%s' % branding_component


def __fetch(filename):
    if __exists(filename):
        return __url(filename)

    return None


COMPONENTS = {'logo': 'logo.jpg',
              'apple': 'apple.jpg',
              'favicon': 'favicon.ico',
              'colours': 'colours.css'}


@register.assignment_tag
def kanisa_branding(branding_component):
    file = COMPONENTS.get(branding_component, None)

    if file is None:
        return None

    return __fetch(file)
