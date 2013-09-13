from django.conf.urls import patterns, url
import kanisa.views.users as views


urlpatterns = patterns(
    '',
    url(r'^$', views.user_management, {}, 'kanisa_manage_users'),
    url(r'^activate/(?P<user_id>\d+)$', views.user_activate, {},
        'kanisa_manage_users_activate'),
)
