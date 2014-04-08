from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import formats
from kanisa.models import (
    Composer,
    RegularEvent,
    Service,
    Song,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
    KanisaDetailView,
    KanisaTemplateView
)


class ServiceBaseView(KanisaAuthorizationMixin):
    def authorization_check(self, user):
        if not user.is_active:
            return False

        return user.can_see_service_plans()

    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_members_services_index')}


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
    kanisa_title = 'Service Planning'
    kanisa_is_root_view = True
    paginate_by = 20

    def get_queryset(self):
        if self.kwargs['show_all']:
            qs = Service.objects.all()
        else:
            qs = Service.future_objects.all()

        return qs.order_by('-event__date')

    def get_context_data(self, **kwargs):
        context = super(ServiceIndexView,
                        self).get_context_data(**kwargs)
        context['showing_all'] = self.kwargs['show_all']

        musician_services = self.request.user.service_musicians.all()
        leader_services = self.request.user.service_set.all()

        all_service_pks = set(
            [s.pk for s in musician_services] +
            [s.pk for s in leader_services]
        )

        for service in context['service_list']:
            service.user_is_involved = service.pk in all_service_pks

        active = [s.user_is_involved for s in context['service_list']]
        context['active_in_some_services'] = any(active)

        return context
index = ServiceIndexView.as_view()


class ServiceDetailView(ServiceBaseView, KanisaDetailView):
    model = Service
    pk_url_kwarg = 'service_pk'
    template_name = 'kanisa/members/services/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['all_songs'] = Song.objects.all()
        return context

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.object.event.date,
                                             "DATE_FORMAT")
        title = 'Plan for %s (%s)' % (unicode(self.object.event),
                                      formatted_date)
        return title
service_detail = ServiceDetailView.as_view()


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

        all_most_popular = most_popular_songs()[:40]

        missing = {}

        for event in events:
            missing[event] = []
            this_event = most_popular_songs(
                service_filter=event
            ).filter(usage__gt=1)

            for song in all_most_popular:
                if song not in this_event:
                    missing[event].append(song)

        context['missing'] = missing

        return context
song_discovery = SongDisoveryView.as_view()


class ComposerDetailView(SongFinderBaseView, KanisaDetailView):
    model = Composer
    template_name = 'kanisa/members/services/composer_detail.html'
    pk_url_kwarg = 'composer_pk'

    def get_context_data(self, **kwargs):
        context = super(ComposerDetailView,
                        self).get_context_data(**kwargs)

        context['song_list'] = self.get_songs()
        return context

    def get_songs(self):
        qs = self.object.song_set.prefetch_related('composers')
        return qs.all()
composer_detail = ComposerDetailView.as_view()
