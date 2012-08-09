from kanisa.models import Sermon, SermonSeries
from django.views.generic.detail import DetailView


class SermonSeriesDetailView(DetailView):
    model = SermonSeries
    template_name = 'kanisa/public/sermons/series.html'


class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'kanisa/public/sermons/sermon.html'
