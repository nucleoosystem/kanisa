from django.conf.urls import patterns, url
import kanisa.views.management.services as views
import kanisa.views.management.services.ccli as ccli_views

urlpatterns = patterns(
    '',
    url(r'^$', views.service_management, {'show_all': False},
        'kanisa_manage_services'),
    url(r'^all/$', views.service_management, {'show_all': True},
        'kanisa_manage_services_all'),

    url(r'^ccli/$', ccli_views.ccli_view, {},
        'kanisa_manage_services_ccli'),

    url(r'^ccli/byusage/$', ccli_views.ccli_view, {'sort': 'usage'},
        'kanisa_manage_services_ccli_by_usage'),

    url(r'^ccli/bytitle/$', ccli_views.ccli_view, {'sort': 'title'},
        'kanisa_manage_services_ccli_by_title'),

    url(r'^service/create/$', views.service_create, {},
        'kanisa_manage_services_create'),

    url(r'^service/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_manage_services_detail'),
    url(r'^service/(?P<service_pk>\d+)/edit/$', views.service_update, {},
        'kanisa_manage_services_update'),
    url(r'^service/(?P<service_pk>\d+)/delete/$', views.service_delete, {},
        'kanisa_manage_services_delete'),
    url(r'^service/(?P<service_pk>\d+)/addsong/$', views.add_song, {},
        'kanisa_manage_services_add_song'),
    url(r'^service/(?P<service_pk>\d+)/createsong/$', views.create_song, {},
        'kanisa_manage_services_create_song'),
    url((r'^service/(?P<service_pk>\d+)/remove/(?P<pk>\d+)/$'),
        views.remove_song, {},
        'kanisa_manage_services_remove_song'),
    url((r'^service/(?P<service_pk>\d+)/move/(?P<song_pk>\d+)/down/$'),
        views.move_down, {},
        'kanisa_manage_services_move_song_down'),
    url((r'^service/(?P<service_pk>\d+)/move/(?P<song_pk>\d+)/up/$'),
        views.move_up, {},
        'kanisa_manage_services_move_song_up'),

    url(r'^band/add/$', views.band_create, {},
        'kanisa_manage_services_create_band'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.band_update, {},
        'kanisa_manage_services_update_band'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.remove_band, {},
        'kanisa_manage_services_remove_band'),

    url(r'^composer/add/$', views.composer_create, {},
        'kanisa_manage_services_create_composer'),
)
