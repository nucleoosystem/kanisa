from django.conf.urls import patterns, url
from kanisa.views.public.diary import (DiaryIndexView,
                                       RegularEventDetailView)


urlpatterns = patterns('',
                       url(r'^$',
                           DiaryIndexView.as_view(),
                           {},
                           'kanisa_public_diary_index'),
                       url(r'^(?P<slug>[a-z0-9-]+)/$',
                           RegularEventDetailView.as_view(),
                           {},
                           'kanisa_public_diary_regularevent_detail'),
                       )
