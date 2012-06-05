from django.conf import settings

KANISA_ADMIN_THUMBS_SIZE = getattr(settings, 'KANISA_ADMIN_THUMBS_SIZE',
                                   '120x120')
