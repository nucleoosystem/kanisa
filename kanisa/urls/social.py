from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required as smr
from kanisa.views.social import SocialIndexView, SocialTwitterPostView


urlpatterns = patterns('',
                       url(r'^$',
                           smr(SocialIndexView.as_view()),
                           {},
                           'kanisa_manage_social'),
                       url(r'^tweet/$',
                           smr(SocialTwitterPostView.as_view()),
                           {},
                           'kanisa_manage_social_twitter_post'),
                       )
