from django.conf.urls import patterns, url
from kanisa.views.xhr.bible import CheckBiblePassageView

urlpatterns = patterns('',
                       url(r'^passage/$',
                           CheckBiblePassageView.as_view(),
                           {},
                           'kanisa_xhr_biblepassage_check'),
                       )
