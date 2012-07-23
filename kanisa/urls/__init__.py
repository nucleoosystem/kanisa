from django.conf.urls import patterns, include, url
from kanisa.views.banners import VisitBannerView
from kanisa.views import KanisaLoginView


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^login/$',
                           KanisaLoginView.as_view(),
                           {},
                           'kanisa_public_login'),
                       url(r'^logout/$',
                           'django.contrib.auth.views.logout',
                           {'template_name': 'kanisa/logout.html', },
                           'kanisa_public_logout'),
                       url(r'^banners/(?P<banner_id>\d+)$',
                           VisitBannerView.as_view(),
                           {},
                           'kanisa_public_banners_visit'),
                       url(r'^manage/',
                           include('kanisa.urls.management')),
                       )
