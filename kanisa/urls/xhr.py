from django.conf.urls import url
from kanisa.views.xhr import bible
from kanisa.views.xhr import diary
from kanisa.views.xhr import services


urlpatterns = [
    url(r'^passage/$', bible.CheckBiblePassageView.as_view(),
        {}, 'kanisa_xhr_biblepassage_check'),
    url(r'^services/bands/$', services.BandInformationView.as_view(),
        {}, 'kanisa_xhr_bandinformation'),
    url(r'^services/events/$', services.EventsView.as_view(),
        {}, 'kanisa_xhr_eventinformation'),
    url(r'^diary/thisweek/$', diary.get_week_public_view,
        {}, 'kanisa_xhr_diary_thisweek'),
]
