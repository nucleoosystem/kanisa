from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage'),

    url(r'^manage/banners/$', 'kanisa.views.manage_banners'),
    url(r'^manage/banners/inactive/$', 'kanisa.views.manage_inactive_banners'),
    url(r'^manage/banners/create/$',
        'kanisa.views.create_banner', {}, 'kanisa_create_banner'),
    url(r'^manage/banners/edit/(?P<banner_id>\d+)$',
        'kanisa.views.edit_banner'),
    url(r'^manage/banners/retire/(?P<banner_id>\d+)$',
        'kanisa.views.retire_banner'),

    url(r'^manage/diary/$', 'kanisa.views.manage_diary'),
)
