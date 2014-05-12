from django.conf.urls import patterns, url
import kanisa.views.members.services as views
import kanisa.views.members.services.bands as band_views
import kanisa.views.members.services.ccli as ccli_views
import kanisa.views.members.services.composers as composer_views
import kanisa.views.members.services.songs as song_views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, {'show_all': False},
        'kanisa_members_services_index'),
    url(r'^all/$', views.index, {'show_all': True},
        'kanisa_members_services_index_all'),

    url(r'^services/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_members_services_detail'),

    url(r'^band/add/$', band_views.band_create, {},
        'kanisa_members_services_create_band'),
    url(r'^bands/(?P<pk>\d+)/edit/$', band_views.band_update, {},
        'kanisa_members_services_update_band'),
    url(r'^bands/(?P<pk>\d+)/remove/$', band_views.remove_band, {},
        'kanisa_members_services_remove_band'),

    url(r'^songs/$', song_views.song_list, {},
        'kanisa_members_services_songs'),
    url(r'^songs/composers/(?P<composer_pk>\d+)/$',
        song_views.composer_detail, {},
        'kanisa_members_services_composer_detail'),
    url(r'^songs/discover/$', song_views.song_discovery, {},
        'kanisa_members_services_song_discovery'),
    url(r'^songs/(?P<song_pk>\d+)/$', song_views.song_detail, {},
        'kanisa_members_services_song_detail'),

    url(r'^ccli/$', ccli_views.ccli_view, {},
        'kanisa_members_services_ccli'),
    url(r'^ccli/byusage/$', ccli_views.ccli_view, {'sort': 'usage'},
        'kanisa_members_services_ccli_by_usage'),
    url(r'^ccli/bytitle/$', ccli_views.ccli_view, {'sort': 'title'},
        'kanisa_members_services_ccli_by_title'),

    url(r'^composer/add/$', composer_views.composer_create, {},
        'kanisa_members_services_create_composer'),
)
