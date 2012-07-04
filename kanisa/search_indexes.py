from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries, SermonSpeaker,
                           Document,
                           Banner,
                           RegularEvent, ScheduledEvent)


class KanisaBaseSearchIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
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


class SermonSpeakerIndex(KanisaBaseSearchIndex):
    title = indexes.CharField()

    def prepare_title(self, obj):
        return '%s %s' % (obj.forename, obj.surname)

site.register(SermonSpeaker, SermonSpeakerIndex)
