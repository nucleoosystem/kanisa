from django.conf.urls import patterns, url
from kanisa.views.media import (MediaIndexView,
                                InlineImageCreateView,
                                InlineImageUpdateView)


urlpatterns = patterns('',
                       url(r'^$',
                           MediaIndexView.as_view(),
                           {},
                           'kanisa_manage_media'),
                       url(r'^create/$',
                           InlineImageCreateView.as_view(),
                           {},
                           'kanisa_manage_media_inlineimage_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           InlineImageUpdateView.as_view(),
                           {},
                           'kanisa_manage_media_inlineimage_update'),
                       )
