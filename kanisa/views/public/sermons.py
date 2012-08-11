from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from kanisa.models import Sermon, SermonSeries


class SermonIndexView(TemplateView):
    template_name = 'kanisa/public/sermons/index.html'

    def get_context_data(self, **kwargs):
        context = super(SermonIndexView,
                        self).get_context_data(**kwargs)

        series = SermonSeries.objects.filter(active=True)
        context['active_series'] = series
        latest_sermons = Sermon.objects.all()
        context['latest_sermons'] = latest_sermons[:5]

        return context


class SermonSeriesDetailView(DetailView):
    model = SermonSeries
    template_name = 'kanisa/public/sermons/series.html'


class SermonDetailView(DetailView):
    model = Sermon
    template_name = 'kanisa/public/sermons/sermon.html'

    def get_object(self, queryset=None):
        object = super(SermonDetailView, self).get_object(queryset)

        if 'series' not in self.kwargs:
            if object.series is not None:
                raise Http404

        return object
