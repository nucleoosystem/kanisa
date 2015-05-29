import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
j = lambda filename: os.path.join(PROJECT_DIR, filename)

DATABASES = {
    'default': {
        # Database name, username and password are set below
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        # Key prefix is set below
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = j('media')
STATIC_ROOT = j('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    j('templates')
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'kanisa.middleware.KanisaPageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'kanisa.context_processors.kanisa_settings',
)

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
    'sorl.thumbnail',
    'crispy_forms',
    'haystack',
    'mptt',
    'recurrence',
    'constance',
    'constance.backends.database',
    'kanisa',
    'djohno',
    'raven.contrib.django.raven_compat',
)

HAYSTACK_SITECONF = 'proj.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = j('whoosh_index')

LOGIN_URL = '/members/account/login/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
AUTH_USER_MODEL = 'kanisa.RegisteredUser'
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.TemporaryFileUploadHandler', )

DATE_FORMAT = 'N j, Y'
TIME_FORMAT = 'P'
SHORT_DATE_FORMAT = 'm/d/Y'
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'TWITTER_ACCESS_TOKEN': ('', 'Configured by using Kanisa.'),
    'TWITTER_ACCESS_SECRET': ('', 'Configured by using Kanisa.'),
}
CONSTANCE_DATABASE_CACHE_BACKEND = 'default'
