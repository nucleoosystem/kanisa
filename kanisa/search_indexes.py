# The import from models causes problems for Django 1.8 - the app
# registry isn't loaded when haystack.autodiscover is called, so we
# end up getting an AppRegistryNotReady exception. We can probably get
# around this by creating an AppConfig class which does the
# autodiscover in the ready method.

from datetime import date
from haystack import indexes
from kanisa.models import (
    BlogPost,
    Page,
    RegularEvent,
    ScheduledEvent,
    Sermon,
    SermonSeries,
)


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True)

    def get_updated_field(self):
        return 'modified'


class ScheduledEventIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return ScheduledEvent

    def index_queryset(self):
        return self.get_model().objects.filter(date__gte=date.today())


class SermonIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return Sermon

    def should_update(self, instance, **kwargs):
        return not instance.in_the_future()

    def index_queryset(self):
        return self.get_model().preached_objects.all()


class BlogPostIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return BlogPost

    def index_queryset(self):
        return self.get_model().published_objects.all()

    def get_updated_field(self):
        return 'updated_date'


class PageIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return Page

    def index_queryset(self):
        return self.get_model().objects.all()


class RegularEventIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return RegularEvent

    def index_queryset(self):
        return self.get_model().objects.all()


class SermonSeriesIndex(KanisaBaseSearchIndex, indexes.Indexable):
    def get_model(self):
        return SermonSeries

    def index_queryset(self):
        return self.get_model().objects.all()
