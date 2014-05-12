from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import formats
from django.views.generic.base import View
from kanisa.forms.services import (
    AddSongToServiceForm,
    CreateSongForm,
)
from kanisa.models import (
    RegularEvent,
    Service,
    Song,
    SongInService,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaDeleteView,
    KanisaDetailView,
    KanisaFormView,
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


class BaseServiceManagementView(ServiceRestrictedBaseView):
    @property
    def service(self):
        if not hasattr(self, "service_"):
            pk = int(self.kwargs['service_pk'])
            self.service_ = get_object_or_404(Service, pk=pk)

        return self.service_


def add_song_to_service(song, service):
    # This code has a race condition that I just don't care about
    # very much.
    qs = SongInService.objects.filter(service=service)
    order = qs.aggregate(Max('order'))['order__max']

    if order is None:
        order = 0

    order += 1

    sis = SongInService.objects.create(song=song,
                                       service=service,
                                       order=order)
    service.songinservice_set.add(sis)


class AddSongView(BaseServiceManagementView, KanisaFormView):
    template_name = 'kanisa/management/create.html'
    form_class = AddSongToServiceForm

    def form_valid(self, form):
        add_song_to_service(form.cleaned_data['song'], self.service)

        if self.request.is_ajax():
            return render_to_response(
                'kanisa/management/services/_song_table.html',
                {'object': self.service,
                 'songs': self.service.songinservice_set.all()},
                context_instance=RequestContext(self.request)
            )

        return super(AddSongView, self).form_valid(form)

    def get_success_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.service.pk, ])

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.service.event.date,
                                             "DATE_FORMAT")
        return 'Add a song to %s (%s)' % (
            unicode(self.service.event),
            formatted_date
        )
add_song = AddSongView.as_view()


class RemoveSongView(BaseServiceManagementView, KanisaDeleteView):
    model = SongInService

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.get_object().delete()
            return render_to_response(
                'kanisa/management/services/_song_table.html',
                {'object': self.service,
                 'songs': self.service.songinservice_set.all()},
                context_instance=RequestContext(request)
            )

        return super(RemoveSongView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.service.pk, ])
remove_song = RemoveSongView.as_view()


class BaseMoveSongView(BaseServiceManagementView, View):
    @property
    def songs(self):
        if not hasattr(self, 'songs_'):
            self.songs_ = self.service.songinservice_set.all()

        return self.songs_

    def get_index_of_song(self):
        pks = [song.pk for song in self.songs]

        return pks.index(int(self.kwargs['song_pk']))

    def swap(self):
        index = self.get_index_of_song()
        target = self.adjust_index(index)

        if target < 0 or target >= len(self.songs):
            raise Http404("Can't move the song to position %d (valid range is "
                          "0 to %d)." % (target, len(self.songs) - 1))

        song = self.songs[index]
        target_song = self.songs[target]
        song.order, target_song.order = target_song.order, song.order
        song.save()
        target_song.save()
        delattr(self, 'songs_')

    def post(self, request, *args, **kwargs):
        self.swap()

        if request.is_ajax():
            return render_to_response(
                'kanisa/management/services/_song_table.html',
                {'object': self.service,
                 'songs': self.songs},
                context_instance=RequestContext(request)
            )

        return HttpResponseRedirect(reverse('kanisa_manage_services_detail',
                                            args=[self.service.pk, ]))


class MoveSongDownView(BaseMoveSongView):
    def adjust_index(self, index):
        return index + 1
move_down = MoveSongDownView.as_view()


class MoveSongUpView(BaseMoveSongView):
    def adjust_index(self, index):
        return index - 1
move_up = MoveSongUpView.as_view()


class CreateSongView(BaseServiceManagementView, KanisaCreateView):
    form_class = CreateSongForm
    kanisa_title = 'Add a New Song'

    def form_valid(self, form):
        rval = super(KanisaCreateView, self).form_valid(form)
        add_song_to_service(self.object, self.service)
        return rval

    def get_success_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.service.pk, ])
create_song = CreateSongView.as_view()
