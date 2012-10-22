from django.conf.urls import patterns, url
import kanisa.views.xhr.media as views


urlpatterns = patterns('',
                       url(r'^images/$',
                           views.list_inline_images,
                           {},
                           'kanisa_manage_xhr_media_inline_images'),
                       url(r'^images/(?P<pk>\d+)$',
                           views.inline_image_detail,
                           {},
                           'kanisa_manage_xhr_media_inline_images_detail'),
                       url(r'^attachments/$',
                           views.list_attachments,
                           {},
                           'kanisa_manage_xhr_media_attachments'),
                       )
