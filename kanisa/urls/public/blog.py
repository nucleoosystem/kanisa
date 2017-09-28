from django.conf.urls import url
import kanisa.views.public.blog as views
from kanisa.views.public.blog.feed import LatestEntriesFeed


urlpatterns = [
    url(r'^$', views.blog_index, {}, 'kanisa_public_blog_index'),
    url(r'^(?P<year>\d{4})/$',
        views.blog_year, {},
        'kanisa_public_blog_year'),
    url(r'^(?P<year>\d{4})/(?P<slug>[a-z0-9-]+)/$',
        views.blog_detail, {},
        'kanisa_public_blog_detail'),
    url(r'^rss/$', LatestEntriesFeed(),
        {}, 'kanisa_public_blog_rss'),
]
