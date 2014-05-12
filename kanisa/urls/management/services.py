from django.conf.urls import patterns, url
import kanisa.views.management.services as views

urlpatterns = patterns(
    '',
    url(r'^$', views.service_management, {'show_all': False},
        'kanisa_manage_services'),
    url(r'^all/$', views.service_management, {'show_all': True},
        'kanisa_manage_services_all'),

    url(r'^service/create/$', views.service_create, {},
        'kanisa_manage_services_create'),

    url(r'^service/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_manage_services_detail'),
    url(r'^service/(?P<service_pk>\d+)/edit/$', views.service_update, {},
        'kanisa_manage_services_update'),
    url(r'^service/(?P<service_pk>\d+)/delete/$', views.service_delete, {},
        'kanisa_manage_services_delete'),
)
