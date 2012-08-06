from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^account/',
                           include('kanisa.urls.public.account')),
                       url(r'^banners/',
                           include('kanisa.urls.public.banners')),
                       url(r'^manage/',
                           include('kanisa.urls.management')),
                       url(r'^xhr/',
                           include('kanisa.urls.xhr')),
                       )
