from kanisa.models import Sermon, SermonSeries
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView


class SermonIndexView(TemplateView):
    template_name = 'kanisa/public/sermons/index.html'

    def get_context_data(self, **kwargs):
        context = super(SermonIndexView,
                        self).get_context_data(**kwargs)

        series = SermonSeries.objects.filter(active=True)
        context['active_series'] = series
        latest_sermons = Sermon.objects.all()
        latest_sermons = latest_sermons.filter(series__isnull=False)
        context['latest_sermons'] = latest_sermons

        return context


class SermonSeriesDetailView(DetailView):
    model = SermonSeries
    template_name = 'kanisa/public/sermons/series.html'


class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'kanisa/public/sermons/sermon.html'
