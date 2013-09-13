from django.conf.urls import patterns, include, url
from kanisa.views import KanisaIndexView


urlpatterns = patterns(
    '',
    url(r'^$', KanisaIndexView.as_view(), {}, 'kanisa_public_index'),
    url(r'^account/', include('kanisa.urls.public.account')),
    url(r'^banners/', include('kanisa.urls.public.banners')),
    url(r'^diary/', include('kanisa.urls.public.diary')),
    url(r'^manage/', include('kanisa.urls.management')),
    url(r'^members/', include('kanisa.urls.members')),
    url(r'^search/', include('kanisa.urls.public.search')),
    url(r'^sermons/', include('kanisa.urls.public.sermons')),
    url(r'^xhr/', include('kanisa.urls.xhr')),
)
