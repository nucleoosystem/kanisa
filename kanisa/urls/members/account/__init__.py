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
        'kanisa_members_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'kanisa/auth/logout.html', },
        'kanisa_members_logout'),

    url(r'^modify/$', KanisaAccountModificationView.as_view(), {},
        'kanisa_members_account_modify'),

    url(r'^registration/$', KanisaRegistrationView.as_view(), {},
        'kanisa_members_registration'),
    url(r'^registration/thanks/$', KanisaRegistrationThanksView.as_view(), {},
        'kanisa_members_registration_thanks'),

    url(r'^auth/', include('kanisa.urls.members.account.auth')),
)
