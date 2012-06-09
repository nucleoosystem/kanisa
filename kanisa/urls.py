from django.conf.urls import patterns, include, url

from kanisa.views.banners import BannerCreateView, BannerUpdateView

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage'),

    url(r'^manage/banners/$', 'kanisa.views.manage_banners'),
    url(r'^manage/banners/inactive/$', 'kanisa.views.manage_inactive_banners'),
    url(r'^manage/banners/create/$',
        BannerCreateView.as_view(), {}, 'kanisa_create_banner'),
    url(r'^manage/banners/edit/(?P<pk>\d+)$',
        BannerUpdateView.as_view(), {}, 'kanisa_update_banner'),
    url(r'^manage/banners/retire/(?P<banner_id>\d+)$',
        'kanisa.views.retire_banner'),

    url(r'^manage/diary/$', 'kanisa.views.manage_diary'),
)
