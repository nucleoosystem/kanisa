from django.core.cache import cache
import kanisa
from kanisa import conf
from kanisa.models import NavigationElement


def kanisa_settings(context):
    elements = cache.get('kanisa_navigation')

    if not elements:
        root_elements = NavigationElement.objects.filter(parent=None)
        elements = [(r, r.children.all()) for r in root_elements]
        cache.set('kanisa_navigation', elements)

    return {
        'KANISA_ALLOW_REGISTRATION': conf.KANISA_REGISTRATION_ALLOWED,
        'KANISA_CHURCH_EMAIL': conf.KANISA_CHURCH_EMAIL,
        'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME,
        'KANISA_GOOGLE_ANALYTICS_KEY': conf.KANISA_GOOGLE_ANALYTICS_KEY,
        'KANISA_NAVIGATION': elements,
        'KANISA_VERSION': kanisa.__version__,
        'KANISA_PRIVACY_URL': conf.KANISA_PRIVACY_URL,
    }
