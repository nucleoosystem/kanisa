from kanisa import conf
from kanisa.models import NavigationElement


def kanisa_settings(context):
    elements = NavigationElement.objects.filter(parent=None)

    return {
        'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME,
        'KANISA_NAVIGATION': elements,
        }
