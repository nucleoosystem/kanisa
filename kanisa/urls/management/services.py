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

    url(r'^service/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_manage_services_detail'),
    url(r'^service/create/$', views.service_create, {},
        'kanisa_manage_services_create'),

    url(r'^band/add/$', views.band_create, {},
        'kanisa_manage_services_create_band'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.band_update, {},
        'kanisa_manage_services_update_band'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.remove_band, {},
        'kanisa_manage_services_remove_band'),

    url(r'^composer/add/$', views.composer_create, {},
        'kanisa_manage_services_create_composer'),
)
