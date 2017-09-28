from django.conf.urls import url
import kanisa.views.management.navigation as views


urlpatterns = [
    url(r'^$', views.navigation_management, {}, 'kanisa_manage_navigation'),
    url(r'^create/$', views.navigation_create, {},
        'kanisa_manage_navigation_create'),
    url(r'^edit/(?P<pk>\d+)$', views.navigation_update, {},
        'kanisa_manage_navigation_update'),
    url(r'^down/(?P<pk>\d+)$', views.navigation_move_down, {},
        'kanisa_manage_navigation_move_down'),
    url(r'^up/(?P<pk>\d+)$', views.navigation_move_up, {},
        'kanisa_manage_navigation_move_up'),
    url(r'^delete/(?P<pk>\d+)$', views.navigation_delete, {},
        'kanisa_manage_navigation_delete'),
]
