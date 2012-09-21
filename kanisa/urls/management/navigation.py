from django.conf.urls import patterns, url
from kanisa.views.navigation import (NavigationElementIndexView,
                                     NavigationElementCreateView,
                                     NavigationElementUpdateView)


urlpatterns = patterns('',
                       url(r'^$',
                           NavigationElementIndexView.as_view(),
                           {},
                           'kanisa_manage_navigation'),
                       url(r'^create/$',
                           NavigationElementCreateView.as_view(),
                           {},
                           'kanisa_manage_navigation_create'),
                       url(r'^edit/(?P<pk>\d+)$',
                           NavigationElementUpdateView.as_view(),
                           {},
                           'kanisa_manage_navigation_update'),
                       )
