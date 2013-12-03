from datetime import datetime
import collections
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from kanisa.forms.services import BandForm, ComposerForm
from kanisa.models import (
    Band,
    RegularEvent,
    Service,
    Song,
    SongInService,
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaDeleteView,
    KanisaListView,
    KanisaTemplateView,
    KanisaUpdateView,
)


class ServiceBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having service planning on your site helps your service '
                   'leaders co-ordinate service plans.')
    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_manage_services')}
    permission = 'kanisa.manage_services'
    kanisa_nav_component = 'services'


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/management/services/index.html'
    kanisa_title = 'Service Planning'
    kanisa_is_root_view = True

    def get_queryset(self):
        if self.kwargs['show_all']:
            return Service.objects.all()
        else:
            return Service.future_objects.all()

    def get_context_data(self, **kwargs):
        context = super(ServiceIndexView,
                        self).get_context_data(**kwargs)
        context['showing_all'] = self.kwargs['show_all']

        songs = Song.objects.all()
        songs = songs.annotate(usage=Count('songinservice'))
        songs = songs.order_by('-usage')
        songs = songs[:5]

        total_songs = SongInService.objects.count()

        if total_songs == 0:
            percents = [0 for s in songs]
        else:
            percents = [(s.usage * 100.0) / total_songs for s in songs]

        context['top_five_songs'] = zip(songs, percents)
        context['bands'] = Band.objects.all()

        return context
service_management = ServiceIndexView.as_view()


class ServiceCCLIView(ServiceBaseView, KanisaTemplateView):
    template_name = 'kanisa/management/services/ccli.html'
    kanisa_title = 'Song Usage Reports'

    def get_selected_event(self):
        if hasattr(self, 'selected_event'):
            return self.selected_event

        if 'event' not in self.request.GET:
            return None

        try:
            pk = int(self.request.GET['event'])
        except ValueError:
            return None

        self.selected_event = RegularEvent.objects.get(pk=pk)
        return self.selected_event

    def get_start_date(self):
        if hasattr(self, 'start_date'):
            return self.start_date

        if 'start_date' not in self.request.GET:
            return None

        try:
            self.start_date = datetime.strptime(self.request.GET['start_date'],
                                                '%m/%d/%Y').date()
        except ValueError:
            return None

        return self.start_date

    def get_end_date(self):
        if hasattr(self, 'end_date'):
            return self.end_date

        if 'end_date' not in self.request.GET:
            return None

        try:
            self.end_date = datetime.strptime(self.request.GET['end_date'],
                                              '%m/%d/%Y').date()
        except ValueError:
            return None

        return self.end_date

    def get_songs(self):
        qs = SongInService.objects.all()

        if self.get_selected_event():
            qs = qs.filter(service__event__event=
                           self.get_selected_event())

        if self.get_start_date():
            qs = qs.filter(service__event__date__gte=
                           self.get_start_date())

        if self.get_end_date():
            qs = qs.filter(service__event__date__lte=
                           self.get_end_date())

        qs = qs.only('song')
        qs = [s.song for s in qs]

        songs = [i for i in collections.Counter(qs).viewitems()]
        songs = sorted(songs, key=lambda s: s[1], reverse=True)

        return songs

    def get_active_filters(self):
        filters = {}
        if self.get_selected_event():
            filters['event'] = self.get_selected_event()

        if self.get_start_date():
            filters['start_date'] = self.get_start_date()

        if self.get_end_date():
            filters['end_date'] = self.get_end_date()

        return filters

    def get_context_data(self, **kwargs):
        context = super(ServiceCCLIView,
                        self).get_context_data(**kwargs)

        services = Service.objects.all().select_related('event',
                                                        'event__event')
        context['filters'] = self.get_active_filters()
        context['events'] = set([s.event.event for s in services])
        context['songs'] = self.get_songs()

        return context
ccli_view = ServiceCCLIView.as_view()


class BandCreateView(ServiceBaseView,
                     KanisaCreateView):
    form_class = BandForm
    kanisa_title = 'Add a Band'
    success_url = reverse_lazy('kanisa_manage_services')
band_create = BandCreateView.as_view()


class BandUpdateView(ServiceBaseView,
                     KanisaUpdateView):
    model = Band
    form_class = BandForm
    success_url = reverse_lazy('kanisa_manage_services')
band_update = BandUpdateView.as_view()


class RemoveBandView(ServiceBaseView,
                     KanisaDeleteView):
    model = Band
    success_url = reverse_lazy('kanisa_manage_services')

    def get_cancel_url(self):
        return self.success_url
remove_band = RemoveBandView.as_view()


class ComposerCreateView(ServiceBaseView,
                         KanisaCreateView):
    form_class = ComposerForm
    kanisa_title = 'Add a Composer'

    def form_valid(self, form):
        if self.is_popup():
            self.object = form.save()
            req = self.request
            tmpl = 'kanisa/management/services/composer_popup_close.html'
            return render_to_response(tmpl,
                                      {'object': self.object},
                                      context_instance=RequestContext(req))

        rval = super(KanisaCreateView, self).form_valid(form)

        messages.success(self.request, self.get_message(form.instance))

        return rval
composer_create = ComposerCreateView.as_view()
