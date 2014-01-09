from django.core.cache import cache
from kanisa import conf
from kanisa import static_conf
from kanisa.models import NavigationElement


def kanisa_settings(context):
    elements = cache.get('kanisa_navigation')

    if not elements:
        root_elements = NavigationElement.objects.filter(parent=None)
        elements = [(r, r.children.all()) for r in root_elements]
        cache.set('kanisa_navigation', elements)

    return {
        'KANISA_ALLOW_REGISTRATION': conf.KANISA_REGISTRATION_ALLOWED,
        'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME,
        'KANISA_CSS_HASH': static_conf.KANISA_CSS_HASH,
        'KANISA_DEBUG_STATIC': conf.KANISA_DEBUG_STATIC,
        'KANISA_MANAGEMENT_JS_HASH': static_conf.KANISA_MANAGEMENT_JS_HASH,
        'KANISA_NAVIGATION': elements,
        'KANISA_PUBLIC_JS_HASH': static_conf.KANISA_PUBLIC_JS_HASH,
    }
