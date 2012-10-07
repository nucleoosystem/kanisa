from django.conf.urls import patterns, url
from kanisa.views.users import (UserManagementView,
                                UserActivateView)

urlpatterns = patterns('',
                       url(r'^$',
                           UserManagementView.as_view(),
                           {},
                           'kanisa_manage_users'),
                       url(r'^activate/(?P<user_id>\d+)$',
                           UserActivateView.as_view(),
                           {},
                           'kanisa_manage_users_activate'),
                       )
