from django.utils.dateformat import DateFormat
from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries,
                           Document,
                           Banner,
                           RegularEvent, ScheduledEvent)
from sorl.thumbnail import get_thumbnail


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    modified = indexes.DateTimeField(model_attr='modified')
    rendered = indexes.CharField(use_template=True)

    def get_updated_field(self):
        return 'modified'


class DocumentIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='title')
site.register(Document, DocumentIndex)


class SermonSeriesIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='title')
site.register(SermonSeries, SermonSeriesIndex)


class SermonIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='title')
site.register(Sermon, SermonIndex)


class BannerIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='headline')

site.register(Banner, BannerIndex)


class RegularEventIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='title')

site.register(RegularEvent, RegularEventIndex)


class ScheduledEventIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='title')

site.register(ScheduledEvent, ScheduledEventIndex)
