from django.conf.urls import patterns, url
from kanisa.views.pages import (PageIndexView,
                                PageCreateView,
                                PageUpdateView,
                                PageDeleteView)

urlpatterns = patterns('',
                       url(r'^$',
                           PageIndexView.as_view(),
                           {},
                           'kanisa_manage_pages'),
                       url(r'^create/$',
                           PageCreateView.as_view(),
                           {},
                           'kanisa_manage_pages_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           PageUpdateView.as_view(),
                           {},
                           'kanisa_manage_pages_update'),
                       url(r'^delete/(?P<pk>\d+)$',
                           PageDeleteView.as_view(),
                           {},
                           'kanisa_manage_pages_delete'),
                       )
