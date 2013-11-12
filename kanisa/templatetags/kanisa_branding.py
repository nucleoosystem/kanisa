import os
from django.core.cache import cache
from django import template
from django.conf import settings


register = template.Library()


COMPONENTS = {
    'logo': {
        'filename': 'logo.jpg',
        'verbose_name': 'Site Logo',
        'sizes': ['480x140', ],
    },
    'apple': {
        'filename': 'apple.jpg',
        'verbose_name': 'Apple Icons',
        'sizes': ['144x144', '114x114', '72x72', '57x57', ],
    },
    'favicon':  {
        'filename': 'favicon.ico',
        'verbose_name': 'Site Favicon',
        'sizes': ['32x32', ],
    },
    'colours':  {
        'filename': 'colours.css',
        'verbose_name': 'Colour settings'
    },
}


class BrandingInformation(object):
    def __init__(self, component):
        if component not in COMPONENTS:
            raise ValueError("Bad branding key: %s." % component)

        self.component = component
        self.url = self.get_cached_url()
        self.sizes = COMPONENTS[self.component].get('sizes', [])
        template_prefix = 'kanisa/management/branding/notes/'
        self.template_name = '%s/_%s.html' % (template_prefix, component)
        self.verbose_name = COMPONENTS[self.component]['verbose_name']

    def get_cached_url(self):
        file = COMPONENTS[self.component]['filename']

        cache_key = 'kanisa_branding_component:%s' % file
        url = cache.get(cache_key)

        if url is not None:
            return url

        url = self.__fetch(file)

        if url is None:
            return url

        # Cache these URLs for 10 minutes - chances are they won't
        # disappear, but on the off-chance they do, let's not keep
        # serving non-existent files forever.
        cache.set(cache_key, url, 600)
        return url

    def __exists(self, branding_component):
        path = os.path.join(settings.MEDIA_ROOT,
                            'branding',
                            '%s' % branding_component)

        return os.path.exists(path)

    def __url(self, branding_component):
        return 'branding/%s' % branding_component

    def __fetch(self, filename):
        if self.__exists(filename):
            return self.__url(filename)

        return None


@register.assignment_tag
def kanisa_branding(branding_component):
    try:
        brand = BrandingInformation(branding_component)
    except ValueError:
        return None

    return brand
