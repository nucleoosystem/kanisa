from kanisa.models import SermonSeries
from django.views.generic.detail import DetailView


class SermonSeriesDetailView(DetailView):
    model = SermonSeries
    template_name = 'kanisa/public/sermons/series.html'
