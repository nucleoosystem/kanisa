from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage'),
    url(r'^manage/banners/$', 'kanisa.views.manage_banners')
)
