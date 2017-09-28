from django.conf.urls import url
import kanisa.views.public.diary as views


urlpatterns = [
    url(r'^$', views.diary_index, {}, 'kanisa_public_diary_index'),
    url(r'^printable/$', views.diary_printable_redirect, {},
        'kanisa_public_diary_printable_redirect'),
    url(r'^printable/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$',
        views.diary_printable, {},
        'kanisa_public_diary_printable'),
    url(r'^contact/$', views.diary_contact, {},
        'kanisa_public_diary_contact'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', views.regular_event_detail, {},
        'kanisa_public_diary_regularevent_detail'),
    url(r'^specials/(?P<pk>[0-9]+)/$', views.scheduled_event_detail, {},
        'kanisa_public_diary_scheduledevent_detail'),
]
