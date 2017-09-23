import hashlib
import json
import os
import shutil
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
    'podcast': {
        'filename': 'podcast.jpg',
        'verbose_name': 'Podcast Logo',
        'sizes': ['1400x1400', ],
    },
    'favicon':  {
        'filename': 'favicon.ico',
        'verbose_name': 'Site Favicon',
        'sizes': ['32x32', ],
    },
    'seasonal': {
        'filename': 'seasonal.jpg',
        'verbose_name': 'Seasonal Header',
        'sizes': ['960x140', ],
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


def flush_brand_colours(colours):
    with open(get_brand_colours_filename(), 'w') as destination:
        destination.write(json.dumps(colours))

    rendered = render_to_string('kanisa/_branding.html',
                                get_brand_colours())

    destination_name = get_branding_disk_file('colours.css')

    with open(destination_name, 'w') as destination:
        destination.write(rendered)


def ensure_branding_directory_exists():
    try:
        os.makedirs(get_branding_disk_file(''))
    except OSError:
        pass


def get_available_colours():
    return {
        'logo_background': 'Used in the header bar alongside your logo.',
        'link_colour': 'Used as the colour for links.',
    }


class BrandingInformation(object):
    def __init__(self, component):
        if component not in BRANDING_COMPONENTS:
            raise ValueError("Bad branding key: %s." % component)

        self.component = component
        self.sizes = BRANDING_COMPONENTS[self.component].get('sizes', [])
        self.verbose_name = BRANDING_COMPONENTS[self.component]['verbose_name']

    @property
    def template_name(self):
        template_prefix = 'kanisa/management/branding/notes/'
        template_name = '%s/_%s.html' % (template_prefix, self.component)

        try:
            get_template(template_name)
            return template_name
        except TemplateDoesNotExist:
            return None

    @property
    def url(self):
        url = self.__fetch()

        if url is None:
            return url

        return url

    def __file_exists(self):
        path = get_branding_disk_file(
            BRANDING_COMPONENTS[self.component]['filename']
        )

        return os.path.exists(path)

    def __url(self):
        filename = BRANDING_COMPONENTS[self.component]['filename']
        filehash = self.__filehash()

        if self.component == 'colours':
            return 'kanisa/branding/%s?%s' % (filename, filehash)

        filebase, extension = os.path.splitext(filename)
        hashed_filename = '%s/%s%s' % (
            filebase, filehash, extension
        )
        hashed_disk_file = get_branding_disk_file(hashed_filename)

        if not os.path.exists(hashed_disk_file):
            thedir, _ = os.path.split(hashed_disk_file)

            try:
                os.makedirs(thedir)
            except OSError:
                pass

            shutil.copyfile(
                get_branding_disk_file(filename),
                hashed_disk_file
            )

        return 'kanisa/branding/%s' % hashed_filename

    def clear_cached_hash(self):
        cache_key = self.__get_cache_key()
        cache.delete(cache_key)

    def __get_cache_key(self):
        return 'kanisa_branding_component:%s' % self.component

    def __filehash(self):
        cache_key = self.__get_cache_key()
        cached_hash = cache.get(cache_key)

        if cached_hash:
            return cached_hash

        content = open(get_branding_disk_file(
            BRANDING_COMPONENTS[self.component]['filename']
        ), 'rb').read()
        md5 = hashlib.md5(content)
        filehash = md5.hexdigest()[:12]

        cache.set(cache_key, filehash, 600)

        return filehash

    def __fetch(self):
        if not self.__file_exists():
            return None

        return self.__url()
