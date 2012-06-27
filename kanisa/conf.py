from django.conf import settings

KANISA_ADMIN_THUMBS_SIZE = getattr(settings, 'KANISA_ADMIN_THUMBS_SIZE',
                                   '60x60')

KANISA_CHURCH_NAME = getattr(settings,
                             'KANISA_CHURCH_NAME',
                             'Your Church')
