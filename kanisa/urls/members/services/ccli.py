from django.conf.urls import url
import kanisa.views.members.services.ccli as views


urlpatterns = [
    url(r'^$', views.ccli_view, {},
        'kanisa_members_services_ccli'),
    url(r'^byusage/$', views.ccli_view, {'sort': 'usage'},
        'kanisa_members_services_ccli_by_usage'),
    url(r'^bytitle/$', views.ccli_view, {'sort': 'title'},
        'kanisa_members_services_ccli_by_title'),
]
