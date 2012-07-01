from haystack import indexes
from haystack import site
from kanisa.models import Sermon, SermonSeries, Document, Banner
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
