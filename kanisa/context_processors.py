from django.core.cache import cache
from kanisa import conf
from kanisa.models import NavigationElement


def kanisa_settings(context):
    elements = cache.get('kanisa_navigation')

    if not elements:
        elements = NavigationElement.objects.filter(parent=None)
        cache.set('kanisa_navigation', elements)

    return {
        'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME,
        'KANISA_NAVIGATION': elements,
        }
