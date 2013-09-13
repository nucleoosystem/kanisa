from django.conf.urls import patterns, url
import kanisa.views.pages as views


urlpatterns = patterns(
    '',
    url(r'^$', views.page_management, {}, 'kanisa_manage_pages'),
    url(r'^create/$', views.page_create, {}, 'kanisa_manage_pages_create'),
    url(r'^edit/(?P<pk>\d+)$', views.page_update, {},
        'kanisa_manage_pages_update'),
    url(r'^delete/(?P<pk>\d+)$', views.page_delete, {},
        'kanisa_manage_pages_delete'),
)
