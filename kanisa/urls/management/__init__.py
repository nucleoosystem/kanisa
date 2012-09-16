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
                           include('kanisa.urls.management.banners')),
                       url(r'^branding/',
                           include('kanisa.urls.management.branding')),
                       url(r'^diary/',
                           include('kanisa.urls.management.diary')),
                       url(r'^documents/',
                           include('kanisa.urls.management.documents')),
                       url(r'^pages/',
                           include('kanisa.urls.management.pages')),
                       url(r'^sermons/',
                           include('kanisa.urls.management.sermons')),
                       url(r'^social/',
                           include('kanisa.urls.management.social')),
                       url(r'^users/',
                           include('kanisa.urls.management.users')),
                       url(r'^xhr/',
                           include('kanisa.urls.management.xhr')),
                       )
