from django.conf.urls import patterns, url
from kanisa.views.public.sermons import SermonSeriesDetailView


urlpatterns = patterns('',
                       url(r'^(?P<slug>[a-z-]+)$',
                           SermonSeriesDetailView.as_view(),
                           {},
                           'kanisa_public_sermon_series_detail'),
                       )
