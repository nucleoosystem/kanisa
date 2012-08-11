from django.conf.urls import patterns, url
from kanisa.views.public.diary import RegularEventDetailView


urlpatterns = patterns('',
                       url(r'^(?P<slug>[a-z0-9-]+)/$',
                           RegularEventDetailView.as_view(),
                           {},
                           'kanisa_public_diary_regularevent_detail'),
                       )
