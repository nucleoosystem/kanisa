from django.conf.urls import patterns, url
import kanisa.views.members.services as views


urlpatterns = patterns('',
                       url(r'^$',
                           views.index,
                           {'show_all': False},
                           'kanisa_members_services_index'),
                       url(r'^all/$',
                           views.index,
                           {'show_all': True},
                           'kanisa_members_services_index_all'),
                       )
