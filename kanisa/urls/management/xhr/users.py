from django.conf.urls import patterns, url
import kanisa.views.xhr.users as views


urlpatterns = patterns('',
                       url(r'^permissions/$',
                           views.assign_permission,
                           {},
                           'kanisa_manage_xhr_assign_permission'),
                       )
