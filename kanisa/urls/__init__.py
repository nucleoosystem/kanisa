from django.conf.urls import patterns, include, url
from kanisa.views import (KanisaManagementIndexView,
                          KanisaSearchView)
from kanisa.views.banners import VisitBannerView


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^banners/(?P<banner_id>\d+)$',
                           VisitBannerView.as_view(),
                           {},
                           'kanisa_public_banners_visit'),
                       url(r'^manage/$',
                           KanisaManagementIndexView.as_view(),
                           {},
                           'kanisa_manage_index'),
                       url(r'^manage/search/$',
                           KanisaSearchView.as_view(),
                           {},
                           'kanisa_manage_search'),
                       url(r'^manage/banners/',
                           include('kanisa.urls.banners')),
                       url(r'^manage/diary/',
                           include('kanisa.urls.diary')),
                       url(r'^manage/sermons/',
                           include('kanisa.urls.sermons')),
                       url(r'^manage/documents/',
                           include('kanisa.urls.documents')),
                       url(r'^manage/social/',
                           include('kanisa.urls.social')),
                       url(r'^manage/xhr/',
                           include('kanisa.urls.xhr')),
                       )
