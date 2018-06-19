from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils import formats
from django.views.generic.base import View
from kanisa.forms.services import (
    AddSongToServiceForm,
    CreateSongForm,
    ServiceForm,
)
from kanisa.models import (
    Service,
    Song,
    SongInService,
)
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaDeleteView,
    KanisaDetailView,
    KanisaFormView,
    KanisaUpdateView,
)
from kanisa.views.members.services import (
    ServiceBaseView,
    ServiceRestrictedBaseView,
    BaseServiceManagementView,
)


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


class ServiceCreateView(ServiceRestrictedBaseView,
                        KanisaCreateView):
    form_class = ServiceForm
    kanisa_title = 'Create a Service Plan'

    def get_template_names(self):
        return ['kanisa/members/form.html', ]

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.object.pk, ])
service_create = ServiceCreateView.as_view()


class ServiceUpdateView(BaseServiceManagementView,
                        KanisaUpdateView):
    form_class = ServiceForm
    model = Service
    pk_url_kwarg = 'service_pk'

    def get_template_names(self):
        return ['kanisa/members/form.html', ]

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])
service_update = ServiceUpdateView.as_view()


class ServiceDeleteView(BaseServiceManagementView,
                        KanisaDeleteView):
    model = Service
    pk_url_kwarg = 'service_pk'

    def get_cancel_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])

    def get_success_url(self):
        return reverse('kanisa_members_services_index')

    def get_template_names(self):
        return ['kanisa/members/delete.html', ]
service_delete = ServiceDeleteView.as_view()


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
            return render(
                self.request,
                'kanisa/members/services/_song_table.html',
                {'object': self.service,
                 'songs': self.service.songinservice_set.all()}
            )

        return super(AddSongView, self).form_valid(form)

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
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
            return render(
                request,
                'kanisa/members/services/_song_table.html',
                {'object': self.service,
                 'songs': self.service.songinservice_set.all()}
            )

        return super(RemoveSongView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
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
            return render(
                request,
                'kanisa/members/services/_song_table.html',
                {'object': self.service,
                 'songs': self.songs}
            )

        return HttpResponseRedirect(reverse('kanisa_members_services_detail',
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
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])
create_song = CreateSongView.as_view()
