from django.conf.urls import patterns, url
import kanisa.views.members.services as views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, {'show_all': False},
        'kanisa_members_services_index'),
    url(r'^all/$', views.index, {'show_all': True},
        'kanisa_members_services_index_all'),
    url(r'^service/(?P<service_pk>\d+)/$', views.service_detail, {},
        'kanisa_members_services_detail'),
    url(r'^songs/$', views.song_list, {},
        'kanisa_members_services_songs'),
    url(r'^songs/(?P<song_pk>\d+)/$', views.song_detail, {},
        'kanisa_members_services_song_detail'),
    url(r'^composers/(?P<composer_pk>\d+)/$', views.composer_detail, {},
        'kanisa_members_services_composer_detail'),
)
