from django.conf.urls import url
import kanisa.views.management.banners as views


urlpatterns = [
    url(r'^$', views.banner_management, {}, 'kanisa_manage_banners'),
    url(r'^inactive/$', views.banner_inactive_management, {},
        'kanisa_manage_banners_inactive'),
    url(r'^create/$', views.banner_create, {},
        'kanisa_manage_banners_create'),
    url(r'^edit/(?P<pk>\d+)$', views.banner_update, {},
        'kanisa_manage_banners_update'),
    url(r'^retire/(?P<banner_id>\d+)$', views.banner_retire, {},
        'kanisa_manage_banners_retire'),
]
