# The import from models causes problems for Django 1.8 - the app
# registry isn't loaded when haystack.autodiscover is called, so we
# end up getting an AppRegistryNotReady exception. We can probably get
# around this by creating an AppConfig class which does the
# autodiscover in the ready method.

from datetime import date
from haystack import indexes
from haystack import site
from kanisa.models import (
    BlogPost,
    Page,
    RegularEvent,
    ScheduledEvent,
    Sermon,
    SermonSeries,
)


class KanisaBaseSearchIndex(indexes.RealTimeSearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True)

    def get_updated_field(self):
        return 'modified'


class ScheduledEventIndex(KanisaBaseSearchIndex):
    def index_queryset(self):
        return ScheduledEvent.objects.filter(date__gte=date.today())


class SermonIndex(KanisaBaseSearchIndex):
    def should_update(self, instance, **kwargs):
        return not instance.in_the_future()

    def index_queryset(self):
        return Sermon.preached_objects.all()


class BlogPostIndex(KanisaBaseSearchIndex):
    def index_queryset(self):
        return BlogPost.published_objects.all()

    def get_updated_field(self):
        return 'updated_date'


site.register(BlogPost, BlogPostIndex)
site.register(Page, KanisaBaseSearchIndex)
site.register(RegularEvent, KanisaBaseSearchIndex)
site.register(ScheduledEvent, ScheduledEventIndex)
site.register(Sermon, SermonIndex)
site.register(SermonSeries, KanisaBaseSearchIndex)
