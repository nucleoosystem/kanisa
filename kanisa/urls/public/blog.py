from django.conf.urls import patterns, url
from kanisa.views.public.blog import (
    BlogIndexView,
    BlogPostDetailView,
)


urlpatterns = patterns(
    '',
    url(r'^$', BlogIndexView.as_view(), {}, 'kanisa_public_blog_index'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', BlogPostDetailView.as_view(), {},
        'kanisa_public_diary_blog_detail'),
)
