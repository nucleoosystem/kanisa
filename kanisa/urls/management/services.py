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

    url(r'^service/(?P<service_pk>\d+)/edit/$', views.service_update, {},
        'kanisa_manage_services_update'),
    url(r'^service/(?P<service_pk>\d+)/addsong/$', views.add_song, {},
        'kanisa_members_services_add_song'),
    url(r'^service/(?P<service_pk>\d+)/createsong/$', views.create_song, {},
        'kanisa_members_services_create_song'),
    url((r'^service/(?P<service_pk>\d+)/remove/(?P<pk>\d+)/$'),
        views.remove_song, {},
        'kanisa_members_services_remove_song'),
    url((r'^service/(?P<service_pk>\d+)/move/(?P<song_pk>\d+)/down/$'),
        views.move_down, {},
        'kanisa_members_services_move_song_down'),
    url((r'^service/(?P<service_pk>\d+)/move/(?P<song_pk>\d+)/up/$'),
        views.move_up, {},
        'kanisa_members_services_move_song_up'),

    url(r'^band/add/$', views.band_create, {},
        'kanisa_manage_services_create_band'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.band_update, {},
        'kanisa_manage_services_update_band'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.remove_band, {},
        'kanisa_manage_services_remove_band'),

    url(r'^composer/add/$', views.composer_create, {},
        'kanisa_manage_services_create_composer'),
)
