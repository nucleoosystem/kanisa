from django.conf.urls import patterns, include, url
from kanisa.views.xhr.pages import (CreatePageView,
                                    ListPagesView)
from kanisa.views.xhr.sermons import MarkSermonSeriesCompleteView
from kanisa.views.xhr.media import (InlineImagesListView,
                                    InlineImagesDetailView,
                                    AttachmentsListView)
from kanisa.views.xhr.users import AssignPermissionView


urlpatterns = patterns('',
                       url(r'^permissions/$',
                           AssignPermissionView.as_view(),
                           {},
                           'kanisa_manage_xhr_assign_permission'),
                       url(r'^navigation/',
                           include('kanisa.urls.management.xhr.navigation')),
                       url(r'^pages/create/$',
                           CreatePageView.as_view(),
                           {},
                           'kanisa_manage_xhr_create_page'),
                       url(r'^pages/list/$',
                           ListPagesView.as_view(),
                           {},
                           'kanisa_manage_xhr_list_pages'),
                       url(r'^sermons/markcomplete/$',
                           MarkSermonSeriesCompleteView.as_view(),
                           {},
                           'kanisa_manage_xhr_sermon_series_complete'),
                       url(r'^media/images/$',
                           InlineImagesListView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_inline_images'),
                       url(r'^diary/',
                           include('kanisa.urls.management.xhr.diary')),
                       url(r'^media/images/(?P<pk>\d+)$',
                           InlineImagesDetailView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_inline_images_detail'),
                       url(r'^media/attachments/$',
                           AttachmentsListView.as_view(),
                           {},
                           'kanisa_manage_xhr_media_attachments'),
                       )
