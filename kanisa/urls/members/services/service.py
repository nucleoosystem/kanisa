from django.conf.urls import url
import kanisa.views.members.services.services as views


urlpatterns = [
    url(r'^(?P<service_pk>\d+)/$',
        views.service_detail, {},
        'kanisa_members_services_detail'),
    url(r'^create/$', views.service_create, {},
        'kanisa_members_services_create'),
    url(r'^(?P<service_pk>\d+)/edit/$',
        views.service_update, {},
        'kanisa_members_services_update'),
    url(r'^(?P<service_pk>\d+)/delete/$',
        views.service_delete, {},
        'kanisa_members_services_delete'),
    url(r'^(?P<service_pk>\d+)/addsong/$', views.add_song, {},
        'kanisa_members_services_add_song'),
    url(r'^(?P<service_pk>\d+)/createsong/$',
        views.create_song, {},
        'kanisa_members_services_create_song'),
    url((r'^(?P<service_pk>\d+)/removesong/(?P<pk>\d+)/$'),
        views.remove_song, {},
        'kanisa_members_services_remove_song'),
    url((r'^(?P<service_pk>\d+)/movedown/(?P<song_pk>\d+)/$'),
        views.move_down, {},
        'kanisa_members_services_move_song_down'),
    url((r'^(?P<service_pk>\d+)/moveup/(?P<song_pk>\d+)/$'),
        views.move_up, {},
        'kanisa_members_services_move_song_up'),
]
