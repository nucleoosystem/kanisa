from django.conf.urls import patterns, url
from kanisa.views.public.sermons import (SermonSeriesDetailView,
                                         SermonDetailView)


urlpatterns = patterns('',
                       url(r'^(?P<slug>[a-z0-9-]+)/$',
                           SermonSeriesDetailView.as_view(),
                           {},
                           'kanisa_public_sermon_series_detail'),
                       url(r'^(?P<series>[a-z0-9-]+)/(?P<slug>[a-z0-9-]+)/$',
                           SermonDetailView.as_view(),
                           {},
                           'kanisa_public_sermon_detail'),
                       )
