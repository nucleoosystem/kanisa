from django.conf.urls import patterns, url
import kanisa.views.social as views


urlpatterns = patterns(
    '',
    url(r'^$', views.social_management, {}, 'kanisa_manage_social'),
    url(r'^twitter/$', views.twitter_management, {},
        'kanisa_manage_social_twitter'),
    url(r'^twitter/create/$', views.scheduled_tweet_create, {},
        'kanisa_manage_social_twitter_create'),
    url(r'^twitter/edit/(?P<pk>\d+)$', views.scheduled_tweet_update, {},
        'kanisa_manage_social_twitter_update'),
    url(r'^twitter/delete/(?P<pk>\d+)$', views.scheduled_tweet_delete, {},
        'kanisa_manage_social_twitter_delete'),
    url(r'^twitter/post/$', views.twitter_post, {},
        'kanisa_manage_social_twitter_post'),
)
