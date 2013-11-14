from django.conf.urls import include, patterns, url
from kanisa.views.public.auth import (
    KanisaAccountModificationView,
    KanisaLoginView,
    KanisaRegistrationView,
    KanisaRegistrationThanksView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', KanisaLoginView.as_view(), {},
        'kanisa_public_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'kanisa/auth/logout.html', },
        'kanisa_public_logout'),

    url(r'^modify/$', KanisaAccountModificationView.as_view(), {},
        'kanisa_public_account_modify'),

    url(r'^registration/$', KanisaRegistrationView.as_view(), {},
        'kanisa_public_registration'),
    url(r'^registration/thanks/$', KanisaRegistrationThanksView.as_view(), {},
        'kanisa_public_registration_thanks'),

    url(r'^password/', include('kanisa.urls.public.password')),
)
