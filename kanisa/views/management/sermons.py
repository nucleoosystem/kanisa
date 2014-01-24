from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms.sermons import (
    SermonForm,
    SermonSeriesForm,
    SermonSpeakerForm
)
from kanisa.models import SermonSeries, Sermon, SermonSpeaker
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaDetailView,
    KanisaDeleteView,
    KanisaListView,
    KanisaUpdateView,
)


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
sermon_management = SermonIndexView.as_view()


class SermonListView(SermonBaseView,
                     KanisaListView):
    model = Sermon
    template_name = 'kanisa/management/sermons/sermons.html'
    kanisa_title = 'Manage Sermons'
sermon_list = SermonListView.as_view()


class SermonSeriesDetailView(SermonBaseView,
                             KanisaDetailView):
    model = SermonSeries
    template_name = 'kanisa/management/sermons/series_detail.html'
sermon_series_detail = SermonSeriesDetailView.as_view()


class SermonSeriesCreateView(SermonBaseView,
                             KanisaCreateView):
    form_class = SermonSeriesForm
    kanisa_title = 'Create a Sermon Series'
    success_url = reverse_lazy('kanisa_manage_sermons')
sermon_series_create = SermonSeriesCreateView.as_view()


class SermonSeriesUpdateView(SermonBaseView,
                             KanisaUpdateView):
    form_class = SermonSeriesForm
    model = SermonSeries
    success_url = reverse_lazy('kanisa_manage_sermons')
sermon_series_update = SermonSeriesUpdateView.as_view()


class SermonSeriesCompleteView(SermonBaseView,
                               RedirectView):
    permanent = False

    def get_redirect_url(self, sermon_id):
        series = get_object_or_404(SermonSeries, pk=sermon_id)
        series.active = False
        series.save()

        message = 'Series "%s" marked as complete.' % unicode(series)
        messages.success(self.request, message)

        return reverse('kanisa_manage_sermons')
sermon_series_mark_complete = SermonSeriesCompleteView.as_view()


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
sermon_create = SermonCreateView.as_view()


class SermonUpdateView(SermonBaseView,
                       KanisaUpdateView):
    form_class = SermonForm
    model = Sermon

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')
sermon_update = SermonUpdateView.as_view()


class SermonDeleteView(SermonBaseView,
                       KanisaDeleteView):
    model = Sermon

    def get_back_url(self):
        object = self.get_object()

        if object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[object.series.pk, ])

        return reverse('kanisa_manager_sermons')

    def get_cancel_url(self):
        return self.get_back_url()

    def delete(self, request, *args, **kwargs):
        url = self.get_back_url()
        self.get_object().delete()

        messages.success(self.request, 'Sermon deleted')
        return HttpResponseRedirect(url)
sermon_delete = SermonDeleteView.as_view()


class SermonSpeakerIndexView(SermonBaseView,
                             KanisaListView):
    model = SermonSpeaker
    queryset = SermonSpeaker.objects.all().order_by('-num_sermons')

    template_name = 'kanisa/management/sermons/speakers.html'
    kanisa_title = 'Manage Speakers'
sermon_speaker_management = SermonSpeakerIndexView.as_view()


class SermonSpeakerCreateView(SermonBaseView,
                              KanisaCreateView):
    form_class = SermonSpeakerForm
    kanisa_title = 'Add a Speaker'
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')
sermon_speaker_create = SermonSpeakerCreateView.as_view()


class SermonSpeakerUpdateView(SermonBaseView,
                              KanisaUpdateView):
    form_class = SermonSpeakerForm
    model = SermonSpeaker
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')
sermon_speaker_update = SermonSpeakerUpdateView.as_view()
