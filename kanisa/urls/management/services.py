from django.conf.urls import patterns, url
import kanisa.views.services as views


urlpatterns = patterns(
    '',
    url(r'^$', views.service_management, {'show_all': False},
        'kanisa_manage_services'),
    url(r'^all/$', views.service_management, {'show_all': True},
        'kanisa_manage_services_all'),
    url(r'^ccli/$', views.ccli_view, {},
        'kanisa_manage_services_ccli'),
)
