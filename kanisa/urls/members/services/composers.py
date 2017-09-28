from django.conf.urls import url
import kanisa.views.members.services.composers as views


urlpatterns = [
    url(r'^add/$', views.composer_create, {},
        'kanisa_members_services_create_composer'),
    url(r'^(?P<composer_pk>\d+)/$',
        views.composer_detail, {},
        'kanisa_members_services_composer_detail'),
]
