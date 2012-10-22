from django.conf.urls import patterns, url
from kanisa.views.xhr.media import (InlineImagesListView,
                                    InlineImagesDetailView,
                                    AttachmentsListView)


urlpatterns = patterns('',
                       url(r'^images/$',
                           InlineImagesListView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_inline_images'),
                       url(r'^images/(?P<pk>\d+)$',
                           InlineImagesDetailView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_inline_images_detail'),
                       url(r'^attachments/$',
                           AttachmentsListView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_attachments'),
                       )
