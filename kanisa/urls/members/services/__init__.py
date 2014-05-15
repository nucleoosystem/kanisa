from django.conf.urls import include, patterns, url
import kanisa.views.members.services as views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, {'show_all': False},
        'kanisa_members_services_index'),
    url(r'^all/$', views.index, {'show_all': True},
        'kanisa_members_services_index_all'),

    url(r'^bands/', include('kanisa.urls.members.services.bands')),
    url(r'^ccli/', include('kanisa.urls.members.services.ccli')),
    url(r'^composers/', include('kanisa.urls.members.services.composers')),
    url(r'^service/', include('kanisa.urls.members.services.service')),
    url(r'^songs/', include('kanisa.urls.members.services.songs')),
)
