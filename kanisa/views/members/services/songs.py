from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from kanisa.forms.services import (
    MergeSongForm,
    UpdateSongForm,
)
from kanisa.models import (
    RegularEvent,
    Service,
    Song,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaDetailView,
    KanisaFormView,
    KanisaUpdateView,
    KanisaListView,
    KanisaTemplateView
)
from kanisa.views.members.services import (
    ServiceBaseView,
    ServiceRestrictedBaseView
)


class SongListView(ServiceBaseView, KanisaListView):
    model = Song
    template_name = 'kanisa/members/services/song_list.html'
    kanisa_title = 'Song Finder'
    paginate_by = 20

    def get_queryset(self):
        return Song.objects.all().prefetch_related('composers')
song_list = SongListView.as_view()


class SongFinderBaseView(ServiceBaseView):
    def get_kanisa_intermediate_crumbs(self):
        return [
            {'url': reverse('kanisa_members_services_songs'),
             'title': 'Song Finder'},
        ]


class SongDetailView(SongFinderBaseView, KanisaDetailView):
    model = Song
    template_name = 'kanisa/members/services/song_detail.html'
    pk_url_kwarg = 'song_pk'

    def get_context_data(self, **kwargs):
        context = super(SongDetailView,
                        self).get_context_data(**kwargs)

        services = self.object.songinservice_set.all()
        services = services.order_by('-service__event__date')
        services = services.select_related('service')
        services = services.select_related('service__event')
        services = services.select_related('service__band_leader')
        context['services'] = services

        return context
song_detail = SongDetailView.as_view()


class SongUpdateView(ServiceRestrictedBaseView,
                     KanisaUpdateView):
    model = Song
    form_class = UpdateSongForm

    def get_template_names(self):
        return ['kanisa/members/form.html', ]

    def get_success_url(self):
        return reverse('kanisa_members_services_song_detail',
                       args=[self.object.pk, ])
song_update = SongUpdateView.as_view()


class SongMergeView(ServiceRestrictedBaseView,
                    KanisaFormView):
    model = Song
    form_class = MergeSongForm

    @property
    def song(self):
        if not hasattr(self, 'song_'):
            self.song_ = get_object_or_404(
                Song,
                pk=self.kwargs['pk']
            )

        return self.song_

    def get_form_kwargs(self):
        return {
            'target_song': self.song
        }

    def get_kanisa_title(self):
        return "Merge song: %s" % self.song.title

    def get_template_names(self):
        return ['kanisa/members/form.html', ]

    def get_success_url(self):
        return reverse('kanisa_members_services_song_detail',
                       args=[self.song.pk, ])
song_merge = SongMergeView.as_view()


class SongDisoveryView(SongFinderBaseView, KanisaTemplateView):
    template_name = 'kanisa/members/services/song_discovery.html'
    kanisa_title = 'Song Discovery'

    def get_context_data(self, **kwargs):
        context = super(SongDisoveryView,
                        self).get_context_data(**kwargs)

        event_type_pks = set(
            item['event__event']
            for item in Service.objects.values('event__event')
        )

        events = RegularEvent.objects.filter(
            pk__in=list(event_type_pks)
        )

        all_songs_past_year = most_popular_songs()

        missing = {}

        for event in events:
            missing[event] = []
            this_event = most_popular_songs(
                service_filter=event
            ).filter(usage__gt=1)

            for song in all_songs_past_year:
                if song not in this_event:
                    missing[event].append(song)

        context['missing'] = missing

        return context
song_discovery = SongDisoveryView.as_view()
