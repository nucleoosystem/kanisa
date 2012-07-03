from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries,
                           Document,
                           Banner,
                           RegularEvent, ScheduledEvent)


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    modified = indexes.DateTimeField(model_attr='modified')
    rendered = indexes.CharField(use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_updated_field(self):
        return 'modified'


site.register(Document, KanisaBaseSearchIndex)
site.register(SermonSeries, KanisaBaseSearchIndex)
site.register(Sermon, KanisaBaseSearchIndex)
site.register(RegularEvent, KanisaBaseSearchIndex)
site.register(ScheduledEvent, KanisaBaseSearchIndex)

class BannerIndex(KanisaBaseSearchIndex):
    title = indexes.CharField(model_attr='headline')

site.register(Banner, BannerIndex)
