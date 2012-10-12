import os
from django.core.cache import cache
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

    cache_key = 'kanisa_branding_component:%s' % file
    url = cache.get(cache_key)

    if url is not None:
        print "Fetched branding URL %s from cache key '%s'." % (url, cache_key)
        return url

    url = __fetch(file)

    if url is None:
        return url

    # Cache these URLs for 10 minutes - chances are they won't
    # disappear, but on the off-chance they do, let's not keep serving
    # non-existent files forever.
    cache.set(cache_key, url, 600)

    return url
