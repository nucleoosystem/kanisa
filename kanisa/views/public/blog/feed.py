from datetime import date, datetime, time
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from kanisa import conf
from kanisa.templatetags.kanisa_markup import kanisa_markdown
from kanisa.models import BlogPost


class LatestEntriesFeed(Feed):
    def title(self):
        return conf.KANISA_BLOG_TITLE

    def description(self):
        return conf.KANISA_BLOG_DESCRIPTION

    def author_name(self):
        return conf.KANISA_CHURCH_NAME

    def feed_copyright(self):
        return (u'Copyright (c) %d %s.'
                % (date.today().year, conf.KANISA_CHURCH_NAME))

    def link(self, obj):
        return reverse('kanisa_public_blog_index')

    def items(self):
        return BlogPost.published_objects.order_by('-publish_date')[:15]

    def item_description(self, item):
        return kanisa_markdown(item.full_text())

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_author_name(self, item):
        if item.author is not None:
            return item.author.get_full_name()

        return self.author_name()

    def item_pubdate(self, item):
        return datetime.combine(item.publish_date, time(0, 0, 0))
