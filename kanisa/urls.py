from django.conf.urls import patterns, include, url
from django.contrib.admin.views.decorators import staff_member_required

from kanisa.views.banners import BannerCreateView, BannerUpdateView
from kanisa.views.diary import (DiaryCreateView, DiaryUpdateView,
                                DiaryRegularEventsView)

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage'),

    # Banners
    url(r'^manage/banners/$',
        'kanisa.views.manage_banners',
        {}, 'kanisa_manage_banners'),
    url(r'^manage/banners/inactive/$',
        'kanisa.views.manage_inactive_banners',
        {}, 'kanisa_manage_inactive_banners'),
    url(r'^manage/banners/create/$',
        staff_member_required(BannerCreateView.as_view()),
        {}, 'kanisa_create_banner'),
    url(r'^manage/banners/edit/(?P<pk>\d+)$',
        staff_member_required(BannerUpdateView.as_view()),
        {}, 'kanisa_update_banner'),
    url(r'^manage/banners/retire/(?P<banner_id>\d+)$',
        'kanisa.views.retire_banner',
        {}, 'kanisa_retire_banner'),

    # Diary
    url(r'^manage/diary/$',
        'kanisa.views.manage_diary',
        {}, 'kanisa_manage_diary'),
    url(r'^manage/diary/regular/$',
        staff_member_required(DiaryRegularEventsView.as_view()),
        {}, 'kanisa_diary_regular_events'),
    url(r'^manage/diary/create/$',
        staff_member_required(DiaryCreateView.as_view()),
        {}, 'kanisa_create_diary'),
    url(r'^manage/diary/edit/(?P<pk>\d+)$',
        staff_member_required(DiaryUpdateView.as_view()),
        {}, 'kanisa_update_diary'),
)
