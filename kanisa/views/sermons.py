from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms.sermons import (SermonSeriesForm,
                                  SermonForm,
                                  SermonSpeakerForm)
from kanisa.models import SermonSeries, Sermon, SermonSpeaker
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDetailView)


class SermonBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having sermons on your site allows people who can\'t make '
                   'services to keep up with what you\'re learning.')
    kanisa_root_crumb = {'text': 'Sermons',
                         'url': reverse_lazy('kanisa_manage_sermons')}
    permission = 'kanisa.manage_sermons'
    kanisa_nav_component = 'sermons'


class SermonIndexView(SermonBaseView,
                      KanisaListView):
    model = SermonSeries
    queryset = SermonSeries.objects.all()

    template_name = 'kanisa/management/sermons/index.html'
    kanisa_title = 'Manage Sermons'
    kanisa_is_root_view = True

    def get_context_data(self, **kwargs):
        context = super(SermonIndexView,
                        self).get_context_data(**kwargs)
        context['standalone'] = Sermon.objects.filter(series__isnull=True)

        return context


class SermonSeriesDetailView(SermonBaseView,
                             KanisaDetailView):
    model = SermonSeries
    template_name = 'kanisa/management/sermons/series_detail.html'


class SermonSeriesCreateView(SermonBaseView,
                             KanisaCreateView):
    form_class = SermonSeriesForm
    kanisa_title = 'Create a Sermon Series'
    success_url = reverse_lazy('kanisa_manage_sermons')


class SermonSeriesUpdateView(SermonBaseView,
                             KanisaUpdateView):
    form_class = SermonSeriesForm
    model = SermonSeries
    success_url = reverse_lazy('kanisa_manage_sermons')


class SermonSeriesCompleteView(SermonBaseView,
                               RedirectView):
    permanent = False

    def get_redirect_url(self, sermon_id):
        series = get_object_or_404(SermonSeries, pk=sermon_id)
        series.active = False
        series.save()

        message = u'Series "%s" marked as complete.' % unicode(series)
        messages.success(self.request, message)

        return reverse('kanisa_manage_sermons')


class SermonCreateView(SermonBaseView,
                       KanisaCreateView):
    form_class = SermonForm
    kanisa_title = 'Upload a Sermon'

    def get_initial(self):
        initial = super(SermonCreateView, self).get_initial()
        initial = initial.copy()

        if 'series' not in self.request.GET:
            return initial

        try:
            series = get_object_or_404(SermonSeries,
                                       pk=self.request.GET['series'])
            initial['series'] = series.pk

            if series.passage:
                initial['passage'] = series.passage

            return initial
        except ValueError:
            raise Http404

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')


class SermonUpdateView(SermonBaseView,
                       KanisaUpdateView):
    form_class = SermonForm
    model = Sermon

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')


class SermonSpeakerIndexView(SermonBaseView,
                             KanisaListView):
    model = SermonSpeaker
    queryset = SermonSpeaker.objects.all().order_by('-num_sermons')

    template_name = 'kanisa/management/sermons/speakers.html'
    kanisa_title = 'Manage Speakers'


class SermonSpeakerCreateView(SermonBaseView,
                              KanisaCreateView):
    form_class = SermonSpeakerForm
    kanisa_title = 'Add a Speaker'
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')


class SermonSpeakerUpdateView(SermonBaseView,
                              KanisaUpdateView):
    form_class = SermonSpeakerForm
    model = SermonSpeaker
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')
