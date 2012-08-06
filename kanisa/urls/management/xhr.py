from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^permissions/$',
                           'kanisa.views.xhr.assign_permission',
                           {},
                           'kanisa_manage_xhr_assign_permission'),
                       url(r'^pages/create/$',
                           'kanisa.views.xhr.create_page',
                           {},
                           'kanisa_manage_xhr_create_page'),
                       url(r'^pages/list/$',
                           'kanisa.views.xhr.list_pages',
                           {},
                           'kanisa_manage_xhr_list_pages'),
                       )
