from django.conf.urls import patterns, url
from kanisa.views.branding import (BrandingManagementIndexView,
                                   BrandingManagementUpdateView,
                                   BrandingManagementUpdateColoursView)


urlpatterns = patterns('',
                       url(r'^$',
                           BrandingManagementIndexView.as_view(),
                           {},
                           'kanisa_manage_branding'),
                       url(r'^images/(?P<resource>[a-z0-9-]+)/$',
                           BrandingManagementUpdateView.as_view(),
                           {},
                           'kanisa_manage_branding_logo'),
                       url(r'^colours/$',
                           BrandingManagementUpdateColoursView.as_view(),
                           {},
                           'kanisa_manage_branding_colours'),
                       )
