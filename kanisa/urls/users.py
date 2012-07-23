from django.conf.urls import patterns, url
from kanisa.views.users import UserManagementView

urlpatterns = patterns('',
                       url(r'^$',
                           UserManagementView.as_view(),
                           {},
                           'kanisa_manage_users'),
                       )
