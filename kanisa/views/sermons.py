from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms import SermonSeriesForm, SermonForm, SermonSpeakerForm
from kanisa.models import SermonSeries, Sermon, SermonSpeaker
from kanisa.views.generic import (StaffMemberRequiredMixin,
                                  KanisaCreateView, KanisaUpdateView,
                                  KanisaListView, KanisaDetailView)


class SermonBaseView:
    kanisa_lead = ('Having sermons on your site allows people who can\'t make '
                   'services to keep up with what you\'re learning.')
    kanisa_root_crumb = {'text': 'Sermons',
                         'url': reverse_lazy('kanisa_manage_sermons')}


class SermonIndexView(StaffMemberRequiredMixin,
                      KanisaListView, SermonBaseView):
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


class SermonSeriesDetailView(StaffMemberRequiredMixin,
                             KanisaDetailView, SermonBaseView):
    model = SermonSeries
    template_name = 'kanisa/management/sermons/series_detail.html'


class SermonSeriesCreateView(StaffMemberRequiredMixin,
                             KanisaCreateView, SermonBaseView):
    form_class = SermonSeriesForm
    kanisa_title = 'Create a Sermon Series'
    success_url = reverse_lazy('kanisa_manage_sermons')


class SermonSeriesUpdateView(StaffMemberRequiredMixin,
                             KanisaUpdateView, SermonBaseView):
    form_class = SermonSeriesForm
    model = SermonSeries
    success_url = reverse_lazy('kanisa_manage_sermons')


class SermonSeriesCompleteView(StaffMemberRequiredMixin,
                               RedirectView):
    permanent = False

    def get_redirect_url(self, sermon_id):
        series = get_object_or_404(SermonSeries, pk=sermon_id)
        series.active = False
        series.save()

        message = u'Series "%s" marked as complete.' % unicode(series)
        messages.success(self.request, message)

        return reverse('kanisa_manage_sermons')


class SermonCreateView(StaffMemberRequiredMixin,
                       KanisaCreateView, SermonBaseView):
    form_class = SermonForm
    kanisa_title = 'Upload a Sermon'

    def get_initial(self):
        initial = super(SermonCreateView, self).get_initial()
        initial = initial.copy()

        if 'series' in self.request.GET:
            initial['series'] = self.request.GET['series']

        return initial

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')


class SermonUpdateView(StaffMemberRequiredMixin,
                       KanisaUpdateView, SermonBaseView):
    form_class = SermonForm
    model = Sermon

    def get_success_url(self):
        if self.object.series:
            return reverse('kanisa_manage_sermons_series_detail',
                           args=[self.object.series.pk, ])
        return reverse('kanisa_manage_sermons')


class SermonSpeakerIndexView(StaffMemberRequiredMixin,
                             KanisaListView, SermonBaseView):
    model = SermonSpeaker
    queryset = SermonSpeaker.objects.all().order_by('-num_sermons')

    template_name = 'kanisa/management/sermons/speakers.html'
    kanisa_title = 'Manage Sermon Speakers'


class SermonSpeakerCreateView(StaffMemberRequiredMixin,
                              KanisaCreateView, SermonBaseView):
    form_class = SermonSpeakerForm
    kanisa_title = 'Add a Speaker'
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')


class SermonSpeakerUpdateView(StaffMemberRequiredMixin,
                              KanisaUpdateView, SermonBaseView):
    form_class = SermonSpeakerForm
    model = SermonSpeaker
    success_url = reverse_lazy('kanisa_manage_sermons_speaker')
