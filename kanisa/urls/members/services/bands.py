from django.conf.urls import url
import kanisa.views.members.services.bands as views


urlpatterns = [
    url(r'^add/$', views.band_create, {},
        'kanisa_members_services_create_band'),
    url(r'^(?P<pk>\d+)/edit/$', views.band_update, {},
        'kanisa_members_services_update_band'),
    url(r'^(?P<pk>\d+)/remove/$', views.remove_band, {},
        'kanisa_members_services_remove_band'),
]
