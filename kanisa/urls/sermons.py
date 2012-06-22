from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required as smr
from kanisa.views.sermons import (SermonIndexView,
                                  SermonSeriesCreateView,
                                  SermonSeriesUpdateView,
                                  SermonSeriesCompleteView)

urlpatterns = patterns('',
                       url(r'^$',
                           smr(SermonIndexView.as_view()),
                           {},
                           'kanisa_manage_sermons'),
                       url(r'^create/$',
                           smr(SermonSeriesCreateView.as_view()),
                           {},
                           'kanisa_manage_sermons_series_create'),
                       url(r'^series/edit/(?P<pk>\d+)$',
                           smr(SermonSeriesUpdateView.as_view()),
                           {},
                           'kanisa_manage_sermons_series_update'),
                       url(r'^complete/(?P<sermon_id>\d+)$',
                           smr(SermonSeriesCompleteView.as_view()),
                           {},
                           'kanisa_manage_sermons_series_complete'),
                       )
