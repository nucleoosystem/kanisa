from django.conf.urls import patterns, url
import kanisa.views.management.diary as views


urlpatterns = patterns(
    '',
    url(r'^$', views.diary_management, {},
        'kanisa_manage_diary'),
    url(r'^series/$', views.diary_event_series, {},
        'kanisa_manage_diary_series'),
    url(r'^series/create/$', views.diary_event_series_create, {},
        'kanisa_manage_diary_series_create'),
    url(r'^series/edit/(?P<pk>\d+)/$', views.diary_event_series_update, {},
        'kanisa_manage_diary_series_update'),
    url(r'^regular/$', views.diary_regular_events, {},
        'kanisa_manage_diary_regularevents'),
    url(r'^regular/create/$', views.diary_regular_event_create, {},
        'kanisa_manage_diary_regular_create'),
    url(r'^regular/edit/(?P<pk>\d+)$', views.diary_regular_event_update, {},
        'kanisa_manage_diary_regular_update'),
    url(r'^regular/bulkedit/(?P<pk>\d+)/$',
        views.diary_regular_event_bulk_edit, {},
        'kanisa_manage_diary_regular_bulkedit'),
    url(r'^scheduled/create/$', views.diary_scheduled_event_create, {},
        'kanisa_manage_diary_scheduled_create'),
    url(r'^scheduled/edit/(?P<pk>\d+)$',
        views.diary_scheduled_event_update, {},
        'kanisa_manage_diary_scheduled_update'),
    url(r'^schedule/(?P<pk>\d+)/(?P<thedate>\d{8})/$',
        views.diary_schedule_regular_event, {},
        'kanisa_manage_diary_schedule_regular_event'),
    url(r'^schedule/all/$', views.diary_schedule_weeks_events, {},
        'kanisa_manage_diary_schedule_weeks_regular_event'),
    url(r'^cancel/(?P<pk>\d+)/$', views.diary_cancel_scheduled_event, {},
        'kanisa_manage_diary_cancel_scheduled_event'),
    url(r'^clone/$', views.diary_scheduled_event_clone, {},
        'kanisa_manage_diary_clone_scheduled_event'),
    url(r'^contacts/$', views.diary_event_contact_management, {},
        'kanisa_manage_diary_contacts'),
    url(r'^contacts/create/$', views.diary_event_contact_create, {},
        'kanisa_manage_diary_contacts_create'),
    url(r'^contacts/edit/(?P<pk>\d+)$', views.diary_event_contact_update, {},
        'kanisa_manage_diary_contacts_update'),
    url(r'^categories/$', views.diary_event_category_management, {},
        'kanisa_manage_diary_categories'),
    url(r'^categories/create/$', views.diary_event_category_create, {},
        'kanisa_manage_diary_categories_create'),
    url(r'^categories/edit/(?P<pk>\d+)$', views.diary_event_category_update,
        {}, 'kanisa_manage_diary_categories_update'),
)
