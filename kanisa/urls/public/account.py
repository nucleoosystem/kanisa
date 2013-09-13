from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from kanisa.forms.auth import KanisaChangePasswordForm
from kanisa.views.public.auth import (
    KanisaLoginView,
    KanisaRegistrationView,
    KanisaRegistrationThanksView,
    KanisaRecoverPasswordView,
    KanisaResetPasswordView,
    KanisaResetPasswordDoneView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', KanisaLoginView.as_view(), {},
        'kanisa_public_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'template_name': 'kanisa/auth/logout.html', },
        'kanisa_public_logout'),

    url(r'^registration/$', KanisaRegistrationView.as_view(), {},
        'kanisa_public_registration'),
    url(r'^registration/thanks/$', KanisaRegistrationThanksView.as_view(), {},
        'kanisa_public_registration_thanks'),

    url(r'^password/$', password_change,
        {'template_name': ('kanisa/management/password_reset.html'),
         'post_change_redirect': '/members/',
         'password_change_form': KanisaChangePasswordForm},
        'kanisa_password_change'),
    url(r'^password/recover/$', KanisaRecoverPasswordView.as_view(), {},
        'kanisa_public_recover_password'),
    url(r'^password/reset/(?P<token>[\w:-]+)/$',
        KanisaResetPasswordView.as_view(), {},
        'kanisa_public_reset_password'),
    url(r'^password/done/$', KanisaResetPasswordDoneView.as_view(), {},
        'kanisa_public_password_reset_done'),
)
