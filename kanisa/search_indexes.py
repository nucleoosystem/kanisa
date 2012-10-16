from datetime import date
from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries,
                           RegularEvent, ScheduledEvent,
                           Page)


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
        return not instance.in_the_future

    def index_queryset(self):
        return Sermon.preached_objects.all()


site.register(SermonSeries, KanisaBaseSearchIndex)
site.register(Sermon, SermonIndex)
site.register(RegularEvent, KanisaBaseSearchIndex)
site.register(ScheduledEvent, ScheduledEventIndex)
site.register(Page, KanisaBaseSearchIndex)
