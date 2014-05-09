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

    url(r'^composer/add/$', views.composer_create, {},
        'kanisa_manage_services_create_composer'),
)
