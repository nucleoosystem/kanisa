from django.conf.urls import patterns, url
from kanisa.views.public.blog import (
    BlogIndexView,
    BlogPostDetailView,
    BlogYearView,
)


urlpatterns = patterns(
    '',
    url(r'^$', BlogIndexView.as_view(), {}, 'kanisa_public_blog_index'),
    url(r'^(?P<year>\d{4})/$',
        BlogYearView.as_view(), {},
        'kanisa_public_blog_year'),
    url(r'^(?P<year>\d{4})/(?P<slug>[a-z0-9-]+)/$',
        BlogPostDetailView.as_view(), {},
        'kanisa_public_blog_detail'),
)
