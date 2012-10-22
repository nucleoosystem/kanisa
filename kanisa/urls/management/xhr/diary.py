from django.conf.urls import patterns, url
from kanisa.views.xhr.diary import (ScheduleRegularEventView,
                                    DiaryGetSchedule)


urlpatterns = patterns('',
                       url(r'^schedule/update/$',
                           ScheduleRegularEventView.as_view(),
                           {},
                           'kanisa_manage_xhr_diary_schedule_regular'),
                       url(r'^schedule/fetch/(?P<date>\d+)/$',
                           DiaryGetSchedule.as_view(),
                           {},
                           'kanisa_manage_xhr_diary_get_schedule'),
                       )
