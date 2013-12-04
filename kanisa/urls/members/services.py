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
)
