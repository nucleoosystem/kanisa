from django.conf.urls import patterns, url
from kanisa.views.public.sermons import (
    SermonArchiveView,
    SermonDetailView,
    SermonDownloadView,
    SermonPodcastDownloadView,
    SermonIndexView,
    SermonSeriesDetailView,
)
from kanisa.views.public.podcast import iTunesPodcastsFeed


urlpatterns = patterns(
    '',
    url(r'^$', SermonIndexView.as_view(), {}, 'kanisa_public_sermon_index'),
    url(r'^archive/$', SermonArchiveView.as_view(), {},
        'kanisa_public_sermon_archive'),
    url(r'^download/(?P<sermon_id>[0-9]+).mp3$',
        SermonDownloadView.as_view(), {}, 'kanisa_public_sermon_download'),
    url(r'^podcasts/enclosures/(?P<sermon_id>[0-9]+).mp3$',
        SermonPodcastDownloadView.as_view(), {},
        'kanisa_public_podcast_sermon_download'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', SermonSeriesDetailView.as_view(), {},
        'kanisa_public_sermon_series_detail'),
    url(r'^standalone/(?P<slug>[a-z0-9-]+)/$', SermonDetailView.as_view(), {},
        'kanisa_public_standalone_sermon_detail'),
    url(r'^(?P<series>[a-z0-9-]+)/(?P<slug>[a-z0-9-]+)/$',
        SermonDetailView.as_view(), {}, 'kanisa_public_sermon_detail'),
    url(r'^podcasts/podcast.xml$',
        iTunesPodcastsFeed(), {}, 'sermon_podcast_itunes'),
)
