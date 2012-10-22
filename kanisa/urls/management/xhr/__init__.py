from django.conf.urls import patterns, include, url
from kanisa.views.xhr.sermons import MarkSermonSeriesCompleteView


urlpatterns = patterns('',
                       url(r'^users/',
                           include('kanisa.urls.management.xhr.users')),
                       url(r'^navigation/',
                           include('kanisa.urls.management.xhr.navigation')),
                       url(r'^pages/',
                           include('kanisa.urls.management.xhr.pages')),
                       url(r'^sermons/markcomplete/$',
                           MarkSermonSeriesCompleteView.as_view(),
                           {},
                           'kanisa_manage_xhr_sermon_series_complete'),
                       url(r'^diary/',
                           include('kanisa.urls.management.xhr.diary')),
                       url(r'^media/',
                           include('kanisa.urls.management.xhr.media')),
                       )
