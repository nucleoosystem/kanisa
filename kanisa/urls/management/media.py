from django.conf.urls import patterns, url
import kanisa.views.media as views


urlpatterns = patterns('',
                       url(r'^$',
                           views.media_management,
                           {},
                           'kanisa_manage_media'),
                       url(r'^create/$',
                           views.media_inline_image_create,
                           {},
                           'kanisa_manage_media_inlineimage_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           views.media_inline_image_update,
                           {},
                           'kanisa_manage_media_inlineimage_update'),
                       )
