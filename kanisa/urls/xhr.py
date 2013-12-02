from django.conf.urls import patterns, url
from kanisa.views.xhr import services
from kanisa.views.xhr import bible

urlpatterns = patterns(
    '',
    url(r'^passage/$', bible.CheckBiblePassageView.as_view(),
        {}, 'kanisa_xhr_biblepassage_check'),
    url(r'^services/bands/$', services.BandInformationView.as_view(),
        {}, 'kanisa_xhr_bandinformation'),
    url(r'^services/events/$', services.EventsView.as_view(),
        {}, 'kanisa_xhr_eventinformation'),
)
