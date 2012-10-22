from django.conf.urls import patterns, url
from kanisa.views.xhr.navigation import (ListNavigationView,
                                         MoveNavigationElementDownView,
                                         MoveNavigationElementUpView)


urlpatterns = patterns('',
                       url(r'^list/$',
                           ListNavigationView.as_view(),
                           {},
                           'kanisa_manage_xhr_list_navigation'),
                       url(r'^up/$',
                           MoveNavigationElementUpView.as_view(),
                           {},
                           'kanisa_manage_xhr_navigation_up'),
                       url(r'^down/$',
                           MoveNavigationElementDownView.as_view(),
                           {},
                           'kanisa_manage_xhr_navigation_down'),
                       )
