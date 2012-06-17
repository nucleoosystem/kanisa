from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^manage/$', 'kanisa.views.manage'),
                       url(r'^manage/banners/',
                           include('kanisa.urls.banners')),
                       url(r'^manage/diary/',
                           include('kanisa.urls.diary')),
                       url(r'^manage/sermons/',
                           include('kanisa.urls.sermons')),
                       )
