from datetime import datetime
import collections
from django.shortcuts import get_object_or_404
from kanisa.models import (
    RegularEvent,
    Service,
    SongInService,
)
from kanisa.views.generic import KanisaTemplateView
from kanisa.views.management.services import ServiceBaseView


class CCLIReport(object):
    selected_event = None
    start_date = None
    end_date = None
    songs = None

    def __init__(self, **kwargs):
        self.selected_event = kwargs.pop('selected_event')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')

        qs = SongInService.objects.all()

        if self.selected_event:
            qs = qs.filter(service__event__event=
                           self.selected_event)

        if self.start_date:
            qs = qs.filter(service__event__date__gte=
                           self.start_date)

        if self.end_date:
            qs = qs.filter(service__event__date__lte=
                           self.end_date)

        qs = qs.only('song')[:50]
        qs = [s.song for s in qs]

        songs = [i for i in collections.Counter(qs).viewitems()]
        songs = sorted(songs,
                       key=lambda s: s[1],
                       reverse=True)
        songs = [(song, self.get_composers(song), usage)
                 for (song, usage) in songs]
        self.songs = songs

    def get_composers(self, song):
        return song.composer_list()


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

        self.selected_event = get_object_or_404(RegularEvent, pk=pk)
        return self.selected_event

    def get_start_date(self):
        if hasattr(self, 'start_date'):
            return self.start_date

        if 'start_date' not in self.request.GET:
            return None

        try:
            self.start_date = datetime.strptime(
                self.request.GET['start_date'],
                '%m/%d/%Y'
            ).date()
        except ValueError:
            return None

        return self.start_date

    def get_end_date(self):
        if hasattr(self, 'end_date'):
            return self.end_date

        if 'end_date' not in self.request.GET:
            return None

        try:
            self.end_date = datetime.strptime(
                self.request.GET['end_date'],
                '%m/%d/%Y'
            ).date()
        except ValueError:
            return None

        return self.end_date

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

        services = Service.objects.all().select_related(
            'event',
            'event__event'
        )
        context['filters'] = self.get_active_filters()
        context['events'] = set([s.event.event for s in services])

        report = CCLIReport(
            selected_event=self.get_selected_event(),
            start_date=self.get_start_date(),
            end_date=self.get_end_date()
        )

        context['report'] = report

        return context
ccli_view = ServiceCCLIView.as_view()
