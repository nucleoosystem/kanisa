from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from kanisa import conf
from kanisa.models import Sermon
from kanisa.utils.branding import BrandingInformation


class iTunesPodcastsFeedGenerator(Rss201rev2Feed):
    def rss_attributes(self):
        return {'version': self._version,
                'xmlns:atom': 'http://www.w3.org/2005/Atom',
                'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        super(iTunesPodcastsFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement('itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement('itunes:author', self.feed['author_name'])
        handler.addQuickElement('itunes:summary', self.feed['description'])
        handler.addQuickElement('itunes:explicit',
                                self.feed['iTunes_explicit'])
        handler.startElement('itunes:owner', {})
        handler.addQuickElement('itunes:name', self.feed['iTunes_name'])
        handler.endElement('itunes:owner')

        if self.feed.get('iTunes_image', None):
            handler.startElement('itunes:image',
                                 {'href': self.feed['iTunes_image']})
            handler.endElement('itunes:image')

        handler.startElement('itunes:category',
                             {'text': 'Religion & Spirituality'})
        handler.startElement('itunes:category',
                             {'text': 'Christianity'})
        handler.endElement('itunes:category')
        handler.endElement('itunes:category')

    def add_item_elements(self, handler, item):
        super(iTunesPodcastsFeedGenerator, self).add_item_elements(handler,
                                                                   item)
        handler.addQuickElement('itunes:summary', item['summary'])
        handler.addQuickElement('itunes:explicit', item['explicit'])


class iTunesPodcastPost():
    def __init__(self, sermon):
        self.id = sermon.id
        self.sermon = sermon
        self.approval_date_time = sermon.created
        self.title = self.get_title()
        self.author = sermon.speaker.name()
        self.summary = sermon.details

        domain = Site.objects.get_current().domain
        url = reverse('kanisa_public_podcast_sermon_download',
                      args=[sermon.id, ])
        self.enclosure_url = 'http://%s%s' % (domain, url)
        self.enclosure_length = sermon.mp3.size
        self.enclosure_mime_type = 'audio/mpeg'
        # self.duration = '%s' % sermon.seconds
        self.explicit = 'clean'
        self.info_url = sermon.url()

    def get_absolute_url(self):
        return self.info_url

    def get_title(self):
        if self.sermon.passage:
            return '%s (%s)' % (self.sermon.title, self.sermon.passage)

        return self.sermon.title


class iTunesPodcastsFeed(Feed):
    """
    A feed of podcasts for iTunes and other compatible podcatchers.
    """

    iTunes_explicit = 'clean'
    feed_type = iTunesPodcastsFeedGenerator

    def title(self):
        return 'Sermons from %s' % conf.KANISA_CHURCH_NAME

    def link(self):
        return 'http://%s' % Site.objects.get_current().domain

    def author_name(self):
        return conf.KANISA_CHURCH_NAME

    def description(self):
        return 'The latest sermons from %s.' % conf.KANISA_CHURCH_NAME

    def image(self):
        branding_information = BrandingInformation('square_logo')
        return branding_information.get_cached_url()

    def items(self):
        """
        Returns a list of items to publish in this feed.
        """
        posts = Sermon.objects.exclude(mp3='').order_by('-date')[:20]
        posts = [iTunesPodcastPost(item) for item in posts]
        return posts

    def feed_extra_kwargs(self, obj):
        extra = {}
        extra['iTunes_name'] = self.title()
        extra['iTunes_explicit'] = self.iTunes_explicit
        extra['iTunes_category'] = 'Religion & Spirituality'
        extra['iTunes_image'] = self.image()

        return extra

    def item_extra_kwargs(self, item):
        return {'summary': item.summary,
                'explicit': item.explicit}

    def item_pubdate(self, item):
        return item.approval_date_time

    def item_enclosure_url(self, item):
        return item.enclosure_url

    def item_enclosure_length(self, item):
        return item.enclosure_length

    def item_enclosure_mime_type(self, item):
        return item.enclosure_mime_type

    def item_description(self, item):
        return item.summary

    def item_title(self, item):
        return item.title

    def item_author_name(self, item):
        return item.author
