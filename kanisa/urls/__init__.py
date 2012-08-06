from django.conf.urls import patterns, include, url
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
                       url(r'^banners/',
                           include('kanisa.urls.public.banners')),
                       url(r'^manage/',
                           include('kanisa.urls.management')),
                       url(r'^xhr/',
                           include('kanisa.urls.xhr')),
                       )
