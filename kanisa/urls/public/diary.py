from django.conf.urls import patterns, url
from kanisa.views.public.diary import (DiaryIndexView,
                                       RegularEventDetailView,
                                       ScheduledEventDetailView)
from kanisa.views.xhr.diary import get_regular_events_view


urlpatterns = patterns('',
                       url(r'^$',
                           DiaryIndexView.as_view(),
                           {},
                           'kanisa_public_diary_index'),
                       url(r'^(?P<slug>[a-z0-9-]+)/$',
                           RegularEventDetailView.as_view(),
                           {},
                           'kanisa_public_diary_regularevent_detail'),
                       url(r'^specials/(?P<pk>[0-9]+)/$',
                           ScheduledEventDetailView.as_view(),
                           {},
                           'kanisa_public_diary_scheduledevent_detail'),
                       url(r'^xhr/regularevents/$',
                           get_regular_events_view,
                           {},
                           'kanisa_public_diary_xhr_regular_events'),
                       )
