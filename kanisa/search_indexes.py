import datetime
from haystack import indexes
from haystack import site
from kanisa.models import SermonSeries, Document, Banner
from sorl.thumbnail import get_thumbnail


class DocumentIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='modified')
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Document.objects.all()

site.register(Document, DocumentIndex)


class SermonSeriesIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    image = indexes.CharField(model_attr='image')
    title = indexes.CharField(model_attr='title')
    details = indexes.CharField(model_attr='details', null=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return SermonSeries.objects.all()

    def prepare_image(self, obj):
        im = get_thumbnail(obj.image, '100x100', crop='center')
        return im.name

site.register(SermonSeries, SermonSeriesIndex)


class BannerIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    image = indexes.CharField(model_attr='image')
    title = indexes.CharField(model_attr='headline')
    details = indexes.CharField(model_attr='contents', null=True)
    url = indexes.CharField(model_attr='url')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Banner.objects.all()

    def prepare_image(self, obj):
        im = get_thumbnail(obj.image, '100x100', crop='center')
        return im.name

site.register(Banner, BannerIndex)
