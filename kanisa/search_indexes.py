from django.utils.dateformat import DateFormat
from haystack import indexes
from haystack import site
from kanisa.models import (Sermon, SermonSeries,
                           Document,
                           Banner,
                           RegularEvent, ScheduledEvent)
from sorl.thumbnail import get_thumbnail


class DocumentIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='modified')
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)

site.register(Document, DocumentIndex)


class SermonSeriesIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    image = indexes.CharField(model_attr='image')
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)
    passage = indexes.CharField(model_attr='passage', null=True)

    def prepare_image(self, obj):
        im = get_thumbnail(obj.image, '100x100', crop='center')
        return im.name

site.register(SermonSeries, SermonSeriesIndex)


class SermonIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)
    speaker = indexes.CharField(model_attr='speaker')
    series = indexes.CharField(model_attr='series', null=True)
    date = indexes.DateField(model_attr='date')
    passage = indexes.CharField(model_attr='passage', null=True)

site.register(Sermon, SermonIndex)


class BannerIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    image = indexes.CharField(model_attr='image')
    title = indexes.CharField(model_attr='headline')
    details = indexes.CharField(model_attr='contents', null=True)
    url = indexes.CharField(model_attr='url')

    def prepare_image(self, obj):
        im = get_thumbnail(obj.image, '100x100', crop='center')
        return im.name

site.register(Banner, BannerIndex)


class RegularEventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)
    start_time = indexes.CharField(model_attr='start_time')
    day = indexes.CharField(model_attr='day')

    def prepare_day(self, obj):
        return obj.get_day_display()

    def prepare_start_time(self, obj):
        return obj.start_time.strftime("%H:%M")

site.register(RegularEvent, RegularEventIndex)


class ScheduledEventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    titleonly = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)
    date = indexes.DateField(model_attr='date')
    start_time = indexes.CharField(model_attr='start_time')
    event = indexes.CharField(model_attr='event', null=True)

    def prepare_start_time(self, obj):
        return obj.start_time.strftime("%H:%M")

    def prepare_title(self, obj):
        thedate = DateFormat(obj.date).format('l, jS F Y')
        return '%s (%s)' % (obj.title, thedate)

site.register(ScheduledEvent, ScheduledEventIndex)
