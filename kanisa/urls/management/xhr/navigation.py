from django.conf.urls import url
import kanisa.views.xhr.navigation as views


urlpatterns = [
    url(r'^list/$', views.list_navigation, {},
        'kanisa_manage_xhr_list_navigation'),
    url(r'^up/$', views.move_navigation_up, {},
        'kanisa_manage_xhr_navigation_up'),
    url(r'^down/$', views.move_navigation_down, {},
        'kanisa_manage_xhr_navigation_down'),
]
