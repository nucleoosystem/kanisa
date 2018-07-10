from datetime import datetime
import collections
from django.shortcuts import get_object_or_404
from kanisa.models import (
    Composer,
    RegularEvent,
    Service,
    Song,
    SongInService,
)
from kanisa.views.generic import KanisaTemplateView
from kanisa.views.members.services import ServiceBaseView


class CCLIReport(object):
    def __init__(self, **kwargs):
        self.selected_event = kwargs.pop('selected_event')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.composer_lists = {}
        self.sort = kwargs.pop('sort')
        show_unsung = kwargs.pop('show_unsung')

        qs = SongInService.objects.all()

        if self.selected_event:
            qs = qs.filter(
                service__event__event=self.selected_event
            )

        if self.start_date:
            qs = qs.filter(
                service__event__date__gte=self.start_date
            )

        if self.end_date:
            qs = qs.filter(
                service__event__date__lte=self.end_date
            )

        qs = qs.select_related('song')
        qs = [s.song for s in qs]

        if show_unsung:
            songs_sung = set(qs)

            all_songs = SongInService.objects.all()

            if self.selected_event:
                all_songs = all_songs.filter(
                    service__event__event=self.selected_event
                )

            all_songs = all_songs.select_related('song')
            all_songs = set([s.song for s in all_songs])
            totally_unsung_songs = Song.objects.all()
            totally_unsung_songs = [
                song for song in totally_unsung_songs
                if song not in qs and song not in all_songs
            ]
            all_songs.update(totally_unsung_songs)

            songs = [
                (s, 0)
                for s in all_songs
                if s not in songs_sung
            ]
        else:
            songs = [i for i in collections.Counter(qs).viewitems()]

        if self.sort == 'title' or show_unsung:
            songs = sorted(songs,
                           key=lambda s: s[0].title,
                           reverse=False)
        else:
            songs = sorted(songs,
                           key=lambda s: s[1],
                           reverse=True)

        self.init_composer_mappings()

        songs = [(song, self.get_composers(song), usage)
                 for (song, usage) in songs]
        self.songs = songs

    def init_composer_mappings(self):
        composers = {c.pk: c.full_name()
                     for c in Composer.objects.all()}
        composer_objects = Song.composers.through.objects.all()

        for item in composer_objects:
            if item.song_id not in self.composer_lists:
                self.composer_lists[item.song_id] = []
            self.composer_lists[item.song_id].append(
                composers[item.composer_id]
            )

    def get_composers(self, song):
        return self.composer_lists.get(song.pk, [])


class ServiceCCLIView(ServiceBaseView, KanisaTemplateView):
    template_name = 'kanisa/members/services/ccli.html'
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

    def get_show_unsung(self):
        return self.request.GET.get('unsung', '0') == '1'

    def get_active_filters(self):
        filters = {}
        if self.get_selected_event():
            filters['event'] = self.get_selected_event()

        if self.get_start_date():
            filters['start_date'] = self.get_start_date()

        if self.get_end_date():
            filters['end_date'] = self.get_end_date()

        if self.get_show_unsung():
            filters['show_unsung'] = self.get_show_unsung()

        return filters

    def get_sort(self):
        return self.kwargs.get('sort', 'usage')

    def get_context_data(self, **kwargs):
        context = super(ServiceCCLIView,
                        self).get_context_data(**kwargs)

        services = Service.objects.all().select_related(
            'event',
            'event__event'
        )
        context['filters'] = self.get_active_filters()
        context['events'] = set([
            s.event.event
            for s in services
            if s.event.event
        ])

        report = CCLIReport(
            selected_event=self.get_selected_event(),
            start_date=self.get_start_date(),
            end_date=self.get_end_date(),
            sort=self.get_sort(),
            show_unsung=self.get_show_unsung()
        )

        context['report'] = report

        return context
ccli_view = ServiceCCLIView.as_view()
