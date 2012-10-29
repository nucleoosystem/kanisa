from django.conf.urls import patterns, url
import kanisa.views.members as views


urlpatterns = patterns('',
                       url(r'^$',
                           views.index,
                           {},
                           'kanisa_members_index'),
                       )
