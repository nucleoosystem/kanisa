from django.conf.urls import patterns, url
from kanisa.views.public.auth import (
    KanisaRecoverPasswordView,
    KanisaResetPasswordView,
    KanisaResetPasswordDoneView,
    KanisaResetPasswordSentView,
    kanisa_members_password_change
)


urlpatterns = patterns(
    '',
    url(r'^$', kanisa_members_password_change, {},
        'kanisa_members_password_change'),
    url(r'^recover/$', KanisaRecoverPasswordView.as_view(), {},
        'kanisa_members_recover_password'),
    url(r'^reset/(?P<token>[\w:-]+)/$',
        KanisaResetPasswordView.as_view(), {},
        'kanisa_members_reset_password'),
    url(r'^recover/(?P<signature>.+)/$',
        KanisaResetPasswordSentView.as_view(), {},
        'kanisa_members_reset_password_sent'),
    url(r'^done/$', KanisaResetPasswordDoneView.as_view(), {},
        'kanisa_members_reset_password_done'),
)
