import json
import os
from django.conf import settings
from django.core.cache import cache
from django.template import TemplateDoesNotExist
from django.template.loader import (
    get_template,
    render_to_string
)


BRANDING_COMPONENTS = {
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


def get_branding_disk_file(filename):
    return os.path.join(settings.MEDIA_ROOT,
                        'kanisa',
                        'branding',
                        filename)


def get_brand_colours_filename():
    return get_branding_disk_file('colours.json')


def get_brand_colours():
    try:
        with open(get_brand_colours_filename(), 'r') as destination:
            return json.loads(destination.read())
    except IOError:
        return {}


def get_cache_key(file):
    return 'kanisa_branding_component:%s' % file


def flush_brand_colours(colours):
    with open(get_brand_colours_filename(), 'w') as destination:
        destination.write(json.dumps(colours))

    rendered = render_to_string('kanisa/_branding.html',
                                get_brand_colours())

    destination_name = get_branding_disk_file('colours.css')

    with open(destination_name, 'w') as destination:
        destination.write(rendered)

    cache.delete(get_cache_key('colours.css'))


def ensure_branding_directory_exists():
    try:
        os.makedirs(get_branding_disk_file(''))
    except OSError:
        pass


def get_available_colours():
    return {
        'logo_background': 'Used in the header bar alongside your logo.',
    }


class BrandingInformation(object):
    def __init__(self, component):
        if component not in BRANDING_COMPONENTS:
            raise ValueError("Bad branding key: %s." % component)

        self.component = component
        self.url = self.get_cached_url()
        self.sizes = BRANDING_COMPONENTS[self.component].get('sizes', [])
        try:
            template_prefix = 'kanisa/management/branding/notes/'
            template_name = '%s/_%s.html' % (template_prefix, component)
            get_template(template_name)
            self.template_name = template_name
        except TemplateDoesNotExist:
            self.template_name = None

        self.verbose_name = BRANDING_COMPONENTS[self.component]['verbose_name']

    def get_cached_url(self):
        file = BRANDING_COMPONENTS[self.component]['filename']

        url = cache.get(get_cache_key(file))

        if url is not None:
            return url

        url = self.__fetch(file)

        if url is None:
            return url

        # Cache these URLs for 10 minutes - chances are they won't
        # disappear, but on the off-chance they do, let's not keep
        # serving non-existent files forever.
        cache.set(get_cache_key(file), url, 600)
        return url

    def __exists(self, branding_component):
        path = get_branding_disk_file(branding_component)

        return os.path.exists(path)

    def __url(self, branding_component):
        return 'kanisa/branding/%s' % branding_component

    def __fetch(self, filename):
        if self.__exists(filename):
            return self.__url(filename)

        return None
