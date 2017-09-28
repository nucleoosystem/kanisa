from django.conf.urls import url
import kanisa.views.xhr.diary as views


urlpatterns = [
    url(r'^schedule/update/$', views.schedule_regular_events, {},
        'kanisa_manage_xhr_diary_schedule_regular'),
    url(r'^schedule/fetch/(?P<date>\d+)/$', views.get_schedule_view, {},
        'kanisa_manage_xhr_diary_get_schedule'),
    url(r'^schedule/find/$', views.diary_scheduled_event_find, {},
        'kanisa_manage_xhr_diary_find_events'),
]
