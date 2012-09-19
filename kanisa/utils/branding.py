import json
import os
from django.conf import settings


def get_brand_colours_filename():
    return os.path.join(settings.MEDIA_ROOT,
                        'branding',
                        'colours.json', )


def get_brand_colours():
    with open(get_brand_colours_filename(), 'r') as destination:
        return json.loads(destination.read())


def flush_brand_colours(colours):
    with open(get_brand_colours_filename(), 'w') as destination:
        destination.write(json.dumps(colours))


def ensure_branding_directory_exists():
    try:
        os.makedirs(os.path.join(settings.MEDIA_ROOT,
                                 'branding'))
    except OSError:
        pass
