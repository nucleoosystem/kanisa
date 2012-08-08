from django.conf.urls import patterns, url
from kanisa.views.xhr.pages import (CreatePageView,
                                    ListPagesView)
from kanisa.views.xhr.sermons import MarkSermonSeriesCompleteView
from kanisa.views.xhr.diary import (ScheduleRegularEventView,
                                    DiaryGetSchedule)
from kanisa.views.xhr.users import AssignPermissionView


urlpatterns = patterns('',
                       url(r'^permissions/$',
                           AssignPermissionView.as_view(),
                           {},
                           'kanisa_manage_xhr_assign_permission'),
                       url(r'^pages/create/$',
                           CreatePageView.as_view(),
                           {},
                           'kanisa_manage_xhr_create_page'),
                       url(r'^pages/list/$',
                           ListPagesView.as_view(),
                           {},
                           'kanisa_manage_xhr_list_pages'),
                       url(r'^sermons/markcomplete/$',
                           MarkSermonSeriesCompleteView.as_view(),
                           {},
                           'kanisa_manage_xhr_sermon_series_complete'),
                       url(r'^diary/schedule/update/$',
                           ScheduleRegularEventView.as_view(),
                           {},
                           'kanisa_manage_xhr_diary_schedule_regular'),
                       url(r'^diary/schedule/fetch/(?P<date>\d+)/$',
                           DiaryGetSchedule.as_view(),
                           {},
                           'kanisa_manage_xhr_diary_get_schedule'),
                       )
