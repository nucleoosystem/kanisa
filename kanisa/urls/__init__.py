from django.conf.urls import patterns, include, url
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = patterns('',
                       url(r'^$', 'kanisa.views.index'),
                       url(r'^manage/$', 'kanisa.views.manage'),
                       url(r'^manage/banners/',
                           include('kanisa.urls.banners')),
                       url(r'^manage/diary/',
                           include('kanisa.urls.diary')),
                       )
