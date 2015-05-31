from django.conf import settings

KANISA_ADMIN_THUMBS_SIZE = getattr(
    settings,
    'KANISA_ADMIN_THUMBS_SIZE',
    '60x60'
)

KANISA_CHURCH_EMAIL = getattr(
    settings,
    'KANISA_CHURCH_EMAIL',
    None
)

KANISA_CHURCH_NAME = getattr(
    settings,
    'KANISA_CHURCH_NAME',
    'Your Church'
)

KANISA_REGISTRATION_ALLOWED = getattr(
    settings,
    'KANISA_ALLOW_REGISTRATION',
    True
)

KANISA_FROM_EMAIL = getattr(
    settings,
    'KANISA_FROM_EMAIL',
    settings.DEFAULT_FROM_EMAIL
)

KANISA_DEBUG_STATIC = getattr(
    settings,
    'KANISA_DEBUG_STATIC',
    settings.DEBUG
)

KANISA_GOOGLE_ANALYTICS_KEY = getattr(
    settings,
    'KANISA_GOOGLE_ANALYTICS_KEY',
    None
)

KANISA_BLOG_TITLE = getattr(
    settings,
    'KANISA_BLOG_TITLE',
    'Updates from %s' % KANISA_CHURCH_NAME
)

KANISA_BLOG_DESCRIPTION = getattr(
    settings,
    'KANISA_BLOG_DESCRIPTION',
    'The latest news and updates from %s.' % KANISA_CHURCH_NAME
)
