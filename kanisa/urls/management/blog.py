from django.conf.urls import url
import kanisa.views.management.blog as views


urlpatterns = [
    url(r'^$', views.blog_management, {}, 'kanisa_manage_blog'),
    url(r'^create/$', views.blog_create, {},
        'kanisa_manage_blog_create'),
    url(r'^edit/(?P<pk>\d+)$', views.blog_update, {},
        'kanisa_manage_blog_update'),
]
