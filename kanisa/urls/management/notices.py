from django.conf.urls import patterns, url
import kanisa.views.management.notices as views


urlpatterns = patterns(
    '',
    url(r'^$', views.notice_management, {}, 'kanisa_manage_notices'),
    url(r'^create/$', views.notice_create, {},
        'kanisa_manage_notice_create'),
    url(r'^edit/(?P<pk>\d+)$', views.notice_update, {},
        'kanisa_manage_notice_update'),
)
