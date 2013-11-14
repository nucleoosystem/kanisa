from django.conf.urls import patterns, url
from kanisa.views.public.auth import (
    KanisaRecoverPasswordView,
    KanisaResetPasswordView,
    KanisaResetPasswordDoneView,
    kanisa_password_change
)


urlpatterns = patterns(
    '',
    url(r'^$', kanisa_password_change, {},
        'kanisa_password_change'),
    url(r'^recover/$', KanisaRecoverPasswordView.as_view(), {},
        'kanisa_public_recover_password'),
    url(r'^reset/(?P<token>[\w:-]+)/$',
        KanisaResetPasswordView.as_view(), {},
        'kanisa_public_reset_password'),
    url(r'^done/$', KanisaResetPasswordDoneView.as_view(), {},
        'kanisa_public_password_reset_done'),
)
