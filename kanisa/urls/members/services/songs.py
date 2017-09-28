from django.conf.urls import url
import kanisa.views.members.services.songs as views


urlpatterns = [
    url(r'^$', views.song_list, {},
        'kanisa_members_services_songs'),
    url(r'^discover/$', views.song_discovery, {},
        'kanisa_members_services_song_discovery'),
    url(r'^(?P<song_pk>\d+)/$', views.song_detail, {},
        'kanisa_members_services_song_detail'),
    url(r'^(?P<pk>\d+)/edit/$', views.song_update, {},
        'kanisa_members_services_song_update'),
    # url(r'^(?P<pk>\d+)/merge/$', views.song_merge, {},
    #     'kanisa_members_services_song_merge'),
]
