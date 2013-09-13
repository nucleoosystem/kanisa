from django.conf.urls import patterns, url
import kanisa.views.branding as views


urlpatterns = patterns(
    '',
    url(r'^$', views.branding_management, {}, 'kanisa_manage_branding'),
    url(r'^images/(?P<resource>[a-z0-9-]+)/$', views.branding_update, {},
        'kanisa_manage_branding_logo'),
    url(r'^colours/$', views.branding_update_colours, {},
        'kanisa_manage_branding_colours'),
)
