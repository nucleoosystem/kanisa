from django.conf.urls import patterns, url
from django.contrib.auth.views import password_change
from kanisa.forms.auth import KanisaChangePasswordForm
from kanisa.views.public.auth import (
    KanisaRecoverPasswordView,
    KanisaResetPasswordView,
    KanisaResetPasswordDoneView
)


urlpatterns = patterns(
    '',
    url(r'^$', password_change,
        {'template_name': ('kanisa/management/password_reset.html'),
         'post_change_redirect': '/members/',
         'password_change_form': KanisaChangePasswordForm},
        'kanisa_password_change'),
    url(r'^recover/$', KanisaRecoverPasswordView.as_view(), {},
        'kanisa_public_recover_password'),
    url(r'^reset/(?P<token>[\w:-]+)/$',
        KanisaResetPasswordView.as_view(), {},
        'kanisa_public_reset_password'),
    url(r'^done/$', KanisaResetPasswordDoneView.as_view(), {},
        'kanisa_public_password_reset_done'),
)
