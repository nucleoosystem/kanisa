from django.conf.urls import patterns, include, url
from django.contrib.admin.views.decorators import staff_member_required

from kanisa.views.banners import (BannerCreateView, BannerUpdateView,
                                  InactiveBannerManagementView,
                                  BannerManagementView,
                                  RetireBannerView)
from kanisa.views.diary import (DiaryCreateView, DiaryUpdateView,
                                DiaryRegularEventsView,
                                DiaryEventIndexView,
                                DiaryScheduleRegularEventView,
                                DiaryCancelScheduledEventView)

urlpatterns = patterns('',
    url(r'^$', 'kanisa.views.index'),
    url(r'^manage/$', 'kanisa.views.manage'),

    # Banners
    url(r'^manage/banners/$',
        staff_member_required(BannerManagementView.as_view()),
        {}, 'kanisa_manage_banners'),
    url(r'^manage/banners/inactive/$',
        staff_member_required(InactiveBannerManagementView.as_view()),
        {}, 'kanisa_manage_banners_inactive'),
    url(r'^manage/banners/create/$',
        staff_member_required(BannerCreateView.as_view()),
        {}, 'kanisa_manage_banners_create'),
    url(r'^manage/banners/edit/(?P<pk>\d+)$',
        staff_member_required(BannerUpdateView.as_view()),
        {}, 'kanisa_manage_banners_update'),
    url(r'^manage/banners/retire/(?P<banner_id>\d+)$',
        staff_member_required(RetireBannerView.as_view()),
        {}, 'kanisa_manage_banners_retire'),

    # Diary
    url(r'^manage/diary/$',
        staff_member_required(DiaryEventIndexView.as_view()),
        {}, 'kanisa_manage_diary'),
    url(r'^manage/diary/regular/$',
        staff_member_required(DiaryRegularEventsView.as_view()),
        {}, 'kanisa_manage_diary_regularevents'),
    url(r'^manage/diary/regular/create/$',
        staff_member_required(DiaryCreateView.as_view()),
        {}, 'kanisa_manage_diary_regular_create'),
    url(r'^manage/diary/regular/edit/(?P<pk>\d+)$',
        staff_member_required(DiaryUpdateView.as_view()),
        {}, 'kanisa_manage_diary_regular_update'),
    url(r'^manage/diary/schedule/(?P<pk>\d+)/(?P<thedate>\d{8})/$',
        staff_member_required(DiaryScheduleRegularEventView.as_view()),
        {}, 'kanisa_manage_diary_schedule_regular_event'),
    url(r'^manage/diary/cancel/(?P<pk>\d+)/$',
        staff_member_required(DiaryCancelScheduledEventView.as_view()),
        {}, 'kanisa_manage_diary_cancel_regular_event'),
)
