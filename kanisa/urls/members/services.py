from django.conf.urls import patterns, url
import kanisa.views.members.services as views


urlpatterns = patterns('',
                       url(r'^$',
                           views.index,
                           {},
                           'kanisa_members_services_index'),
                       )
