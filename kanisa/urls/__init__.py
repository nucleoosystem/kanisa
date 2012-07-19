from django.conf.urls import patterns, include, url
from kanisa.views.banners import VisitBannerView


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^banners/(?P<banner_id>\d+)$',
                           VisitBannerView.as_view(),
                           {},
                           'kanisa_public_banners_visit'),
                       url(r'^manage/',
                           include('kanisa.urls.management')),
                       )
