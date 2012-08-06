from django.conf.urls import patterns, include, url
from kanisa.views import (KanisaManagementIndexView,
                          KanisaSearchView)


urlpatterns = patterns('',
                       url(r'^$',
                           KanisaManagementIndexView.as_view(),
                           {},
                           'kanisa_manage_index'),
                       url(r'^search/$',
                           KanisaSearchView.as_view(),
                           {},
                           'kanisa_manage_search'),

                       url(r'^banners/',
                           include('kanisa.urls.banners')),
                       url(r'^diary/',
                           include('kanisa.urls.diary')),
                       url(r'^documents/',
                           include('kanisa.urls.documents')),
                       url(r'^pages/',
                           include('kanisa.urls.pages')),
                       url(r'^sermons/',
                           include('kanisa.urls.sermons')),
                       url(r'^social/',
                           include('kanisa.urls.social')),
                       url(r'^users/',
                           include('kanisa.urls.users')),
                       url(r'^xhr/',
                           include('kanisa.urls.xhr')),
                       )
