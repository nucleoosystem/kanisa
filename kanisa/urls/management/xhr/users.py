from django.conf.urls import patterns, url
from kanisa.views.xhr.users import AssignPermissionView


urlpatterns = patterns('',
                       url(r'^permissions/$',
                           AssignPermissionView.as_view(),
                           {},
                           'kanisa_manage_xhr_assign_permission'),
                       )
