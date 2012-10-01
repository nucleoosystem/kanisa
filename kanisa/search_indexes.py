from datetime import date
from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries,
                           RegularEvent, ScheduledEvent,
                           Page)


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True)

    def get_updated_field(self):
        return 'modified'


class ScheduledEventIndex(KanisaBaseSearchIndex):
    def index_queryset(self):
        return ScheduledEvent.objects.filter(date__gte=date.today())


site.register(SermonSeries, KanisaBaseSearchIndex)
site.register(Sermon, KanisaBaseSearchIndex)
site.register(RegularEvent, KanisaBaseSearchIndex)
site.register(ScheduledEvent, ScheduledEventIndex)
site.register(Page, KanisaBaseSearchIndex)
