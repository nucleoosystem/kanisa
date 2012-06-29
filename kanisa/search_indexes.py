import datetime
from haystack import indexes
from haystack import site
from kanisa.models import SermonSeries, Document


class DocumentIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='modified')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Document.objects.all()

site.register(Document, DocumentIndex)


class SermonSeriesIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return SermonSeries.objects.all()

site.register(SermonSeries, SermonSeriesIndex)
