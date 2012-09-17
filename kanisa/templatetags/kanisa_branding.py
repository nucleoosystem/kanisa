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


@register.assignment_tag
def kanisa_branding(branding_component):
    if branding_component == 'logo':
        return __fetch('logo.jpg')

    if branding_component == 'apple':
        return __fetch('apple.jpg')

    if branding_component == 'favicon':
        return __fetch('favicon.ico')

    return None
