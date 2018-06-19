DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

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

INSTALLED_APPS = (
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
    'captcha',
    'kanisa',
)

LOGIN_URL = '/members/account/login/'

ROOT_URLCONF = 'tests.tox.urls'

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'kanisa.context_processors.kanisa_settings',
            )
        },
    },
]

import os
PROJECT_DIR = os.path.dirname(__file__)
j = lambda filename: os.path.join(PROJECT_DIR, filename)


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': j('.test_whoosh')
    }
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

DATE_FORMAT = 'N j, Y'
TIME_FORMAT = 'P'
SHORT_DATE_FORMAT = 'm/d/Y'

STATIC_URL = '/fakestatictrees/'

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstrap'

AUTH_USER_MODEL = 'kanisa.RegisteredUser'

SECRET_KEY = 'thisbagismadefromrecycledmaterial'

RECAPTCHA_PUBLIC_KEY = 'MyRecaptchaKey123'
RECAPTCHA_PRIVATE_KEY = 'MyRecaptchaPrivateKey456'
NOCAPTCHA = True
