from django.conf.urls import url
from kanisa.views.public.banners import VisitBannerView


urlpatterns = [
    url(r'^(?P<banner_id>\d+)$',
        VisitBannerView.as_view(),
        {},
        'kanisa_public_banners_visit'),
]
