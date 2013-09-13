from django.conf.urls import patterns, url
import kanisa.views.xhr.diary as views


urlpatterns = patterns(
    '',
    url(r'^schedule/update/$', views.schedule_regular_events, {},
        'kanisa_manage_xhr_diary_schedule_regular'),
    url(r'^schedule/fetch/(?P<date>\d+)/$', views.get_schedule_view, {},
        'kanisa_manage_xhr_diary_get_schedule'),
)
