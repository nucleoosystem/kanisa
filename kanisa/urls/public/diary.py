from django.conf.urls import patterns, url
import kanisa.views.public.diary as views


urlpatterns = patterns(
    '',
    url(r'^$', views.diary_index, {}, 'kanisa_public_diary_index'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', views.regular_event_detail, {},
        'kanisa_public_diary_regularevent_detail'),
    url(r'^specials/(?P<pk>[0-9]+)/$', views.scheduled_event_detail, {},
        'kanisa_public_diary_scheduledevent_detail'),
)
