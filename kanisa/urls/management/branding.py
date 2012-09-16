from django.conf.urls import patterns, url
from kanisa.views.branding import (BrandingManagementIndexView,
                                   BrandingManagementUpdateView)


urlpatterns = patterns('',
                       url(r'^$',
                           BrandingManagementIndexView.as_view(),
                           {},
                           'kanisa_manage_branding'),
                       url(r'^(?P<resource>[a-z0-9-]+)/$',
                           BrandingManagementUpdateView.as_view(),
                           {},
                           'kanisa_manage_branding_logo'),
                       )
