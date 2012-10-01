from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries, SermonSpeaker,
                           Document,
                           RegularEvent, ScheduledEvent,
                           ScheduledTweet,
                           Page)


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    rendered = indexes.CharField(use_template=True)

    def get_updated_field(self):
        return 'modified'


site.register(SermonSeries, KanisaBaseSearchIndex)
site.register(Sermon, KanisaBaseSearchIndex)
site.register(SermonSpeaker, KanisaBaseSearchIndex)
site.register(Document, KanisaBaseSearchIndex)
site.register(RegularEvent, KanisaBaseSearchIndex)
site.register(ScheduledEvent, KanisaBaseSearchIndex)
site.register(ScheduledTweet, KanisaBaseSearchIndex)
site.register(Page, KanisaBaseSearchIndex)
