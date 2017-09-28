from django.conf.urls import url
import kanisa.views.management.sermons as views


urlpatterns = [
    url(r'^$', views.sermon_management, {}, 'kanisa_manage_sermons'),
    url(r'^series/(?P<pk>\d+)$', views.sermon_series_detail, {},
        'kanisa_manage_sermons_series_detail'),
    url(r'^series/create/$', views.sermon_series_create, {},
        'kanisa_manage_sermons_series_create'),
    url(r'^series/edit/(?P<pk>\d+)$', views.sermon_series_update, {},
        'kanisa_manage_sermons_series_update'),
    url(r'^complete/(?P<sermon_id>\d+)$', views.sermon_series_mark_complete,
        {}, 'kanisa_manage_sermons_series_complete'),
    url(r'^sermons/$', views.sermon_list, {},
        'kanisa_manage_sermons_list'),
    url(r'^sermons/create/$', views.sermon_create, {},
        'kanisa_manage_sermons_individual_create'),
    url(r'^sermons/edit/(?P<pk>\d+)$', views.sermon_update, {},
        'kanisa_manage_sermons_individual_update'),
    url(r'^sermons/delete/(?P<pk>\d+)$', views.sermon_delete, {},
        'kanisa_manage_sermons_individual_delete'),
    url(r'^speaker/$', views.sermon_speaker_management, {},
        'kanisa_manage_sermons_speaker'),
    url(r'^speaker/create/$', views.sermon_speaker_create, {},
        'kanisa_manage_sermons_speaker_create'),
    url(r'^speaker/edit/(?P<pk>\d+)$', views.sermon_speaker_update, {},
        'kanisa_manage_sermons_speaker_update'),
]
