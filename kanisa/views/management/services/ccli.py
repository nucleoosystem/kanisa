from datetime import datetime
import collections
from kanisa.models import (
    RegularEvent,
    Service,
    SongInService,
)
from kanisa.views.generic import KanisaTemplateView
from kanisa.views.management.services import ServiceBaseView


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
