from django.conf.urls import patterns, url
from kanisa.views.sermons import SermonSeriesView


urlpatterns = patterns('',
                       url(r'^(?P<slug>[a-z-]+)$',
                           SermonSeriesView.as_view(),
                           {},
                           'kanisa_public_sermon_series'),
                       )
