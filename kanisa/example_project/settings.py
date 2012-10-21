import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
MEDIA_URL = STATIC_URL + "media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)
SECRET_KEY = "incrediblysecretkeyyoushouldchange"
ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'sorl.thumbnail',
    'crispy_forms',
    'haystack',
    'mptt',
    'recurrence',
    'kanisa',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'kanisa.context_processors.kanisa_settings',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'kanisa.middleware.KanisaPageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

DATE_FORMAT = 'j M Y'
TIME_FORMAT = 'P'
SHORT_DATE_FORMAT = 'm/d/Y'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher', )

HAYSTACK_SITECONF = 'example_project.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, "whoosh_index")

USE_TZ = True
LOGIN_URL = '/login/'
