from django.conf.urls import patterns, url
from kanisa.views.public.banners import VisitBannerView


urlpatterns = patterns('',
                       url(r'^(?P<banner_id>\d+)$',
                           VisitBannerView.as_view(),
                           {},
                           'kanisa_public_banners_visit'),
                       )
