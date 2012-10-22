from django.conf.urls import patterns, url
from kanisa.views.xhr.sermons import MarkSermonSeriesCompleteView


urlpatterns = patterns('',
                       url(r'^markcomplete/$',
                           MarkSermonSeriesCompleteView.as_view(),
                           {},
                           'kanisa_manage_xhr_sermon_series_complete'),
                       )
