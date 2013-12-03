from django.conf.urls import patterns, url
import kanisa.views.members.services as views


urlpatterns = patterns(
    '',
    # URLs for members
    url(r'^$', views.index, {'show_all': False},
        'kanisa_members_services_index'),
    url(r'^all/$', views.index, {'show_all': True},
        'kanisa_members_services_index_all'),
    url(r'^service/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_members_services_detail'),

    # URLs for management - these need to be moved
    url(r'^service/create/$', views.service_create, {},
        'kanisa_members_services_create'),
    url(r'^service/(?P<service_pk>\d+)/edit/$', views.service_update, {},
        'kanisa_members_services_update'),
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
    url(r'^composer/add/$', views.composer_create, {},
        'kanisa_members_services_create_composer'),
    url(r'^band/add/$', views.band_create, {},
        'kanisa_members_services_create_band'),
    url(r'^bands/(?P<pk>\d+)/edit/$', views.band_update, {},
        'kanisa_members_services_update_band'),
    url(r'^bands/(?P<pk>\d+)/remove/$', views.remove_band, {},
        'kanisa_members_services_remove_band'),
)
