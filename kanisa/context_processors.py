from django.conf import settings


def kanisa_settings(context):
    return {'KANISA_CHURCH_NAME': getattr(settings, 'KANISA_CHURCH_NAME', 'Your Church') }
