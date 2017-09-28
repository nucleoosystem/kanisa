from django.conf.urls import url
import kanisa.views.xhr.pages as views


urlpatterns = [
    url(r'^create/$', views.create_page, {}, 'kanisa_manage_xhr_create_page'),
    url(r'^list/$', views.list_pages, {}, 'kanisa_manage_xhr_list_pages'),
]
