from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage')
)
