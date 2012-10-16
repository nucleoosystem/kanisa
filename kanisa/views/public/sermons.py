from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from kanisa.models import Sermon, SermonSeries


class SermonIndexView(TemplateView):
    template_name = 'kanisa/public/sermons/index.html'

    def get_context_data(self, **kwargs):
        context = super(SermonIndexView,
                        self).get_context_data(**kwargs)

        series = SermonSeries.objects.filter(active=True)
        context['active_series'] = series
        latest_sermons = Sermon.preached_objects.all()
        context['latest_sermons'] = latest_sermons[:5]
        context['kanisa_title'] = 'Sermons'

        return context


class SermonSeriesDetailView(DetailView):
    model = SermonSeries
    template_name = 'kanisa/public/sermons/series.html'

    def get_context_data(self, **kwargs):
        context = super(SermonSeriesDetailView,
                        self).get_context_data(**kwargs)
        context['kanisa_title'] = unicode(self.object)
        return context


class SermonDetailView(DetailView):
    queryset = Sermon.preached_objects.all()
    template_name = 'kanisa/public/sermons/sermon.html'

    def get_context_data(self, **kwargs):
        context = super(SermonDetailView, self).get_context_data(**kwargs)
        context['kanisa_title'] = unicode(self.object)
        return context

    def get_object(self, queryset=None):
        object = super(SermonDetailView, self).get_object(queryset)

        if 'series' not in self.kwargs:
            if object.series is not None:
                raise Http404
            return object

        if object.series.slug != self.kwargs['series']:
            raise Http404

        return object


class SermonArchiveView(ListView):
    model = Sermon
    template_name = 'kanisa/public/sermons/archive.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SermonArchiveView,
                        self).get_context_data(**kwargs)

        context['kanisa_title'] = 'Sermon Archives'

        return context
