from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import formats
from django.views.generic.base import View
from kanisa.forms.services import (AddSongToServiceForm,
                                   ServiceForm,
                                   CreateSongForm,
                                   ComposerForm)
from kanisa.models import Service, Song, SongInService, ScheduledEvent
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import (KanisaListView,
                                  KanisaDetailView,
                                  KanisaFormView,
                                  KanisaCreateView,
                                  KanisaUpdateView,
                                  KanisaDeleteView)


class ServiceIndexView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
    kanisa_title = 'Service Planning'

    def get_queryset(self):
        if self.kwargs['show_all']:
            return Service.objects.all()
        else:
            return Service.future_objects.all()

    def get_context_data(self, **kwargs):
        context = super(ServiceIndexView,
                        self).get_context_data(**kwargs)
        context['showing_all'] = self.kwargs['show_all']
        return context
index = ServiceIndexView.as_view()


class ServiceDetailView(MembersBaseView, KanisaDetailView):
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
        title = 'Plan for %s (%s)' % (self.object.event.title,
                                      formatted_date)
        return title
service_detail = ServiceDetailView.as_view()


class ServiceCreateView(MembersBaseView,
                        KanisaCreateView):
    form_class = ServiceForm
    kanisa_title = 'Create a Service Plan'

    def get_events_queryset(self):
        if not hasattr(self, 'events'):
            self.events = ScheduledEvent.objects.filter(service__isnull=True)

        return self.events

    def get_form(self, form_class):
        form = super(ServiceCreateView, self).get_form(form_class)
        form.fields['event'].queryset = self.get_events_queryset()

        return form

    def get(self, request, *args, **kwargs):
        events = self.get_events_queryset()

        if not events:
            messages.info(self.request,
                          ("There are no events without a service plan, "
                           "please create an event before adding a service "
                           "plan."))
            return HttpResponseRedirect(reverse('kanisa_members_services_index'))

        return super(ServiceCreateView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.object.pk, ])

    def get_template_names(self):
        return ['kanisa/members/form.html', ]
service_create = ServiceCreateView.as_view()


class BaseServiceManagementView(MembersBaseView):
    @property
    def service(self):
        if hasattr(self, "service_"):
            return self.service_

        self.service_ = get_object_or_404(Service,
                                          pk=int(self.kwargs['service_pk']))

        return self.service_


class ServiceUpdateView(BaseServiceManagementView,
                        KanisaUpdateView):
    form_class = ServiceForm
    model = Service
    template_name = 'kanisa/members/form.html'
    pk_url_kwarg = 'service_pk'

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])
service_update = ServiceUpdateView.as_view()


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
    form_class = AddSongToServiceForm
    template_name = 'kanisa/members/form.html'

    def form_valid(self, form):
        add_song_to_service(form.cleaned_data['song'], self.service)
        return super(AddSongView, self).form_valid(form)

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.service.event.date,
                                             "DATE_FORMAT")
        return 'Add a song to %s (%s)' % (self.service.event.title,
                                          formatted_date)
add_song = AddSongView.as_view()


class RemoveSongView(BaseServiceManagementView, KanisaDeleteView):
    model = SongInService

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])
remove_song = RemoveSongView.as_view()


class BaseMoveSongView(BaseServiceManagementView, View):
    @property
    def songs(self):
        if hasattr(self, 'songs_'):
            return self.songs_

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

    def post(self, request, *args, **kwargs):
        self.swap()

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

    def get_template_names(self):
        return ['kanisa/members/form.html', ]

    def get_success_url(self):
        return reverse('kanisa_members_services_detail',
                       args=[self.service.pk, ])
create_song = CreateSongView.as_view()


class ComposerCreateView(MembersBaseView,
                         KanisaCreateView):
    form_class = ComposerForm
    kanisa_title = 'Add a Composer'

    def form_valid(self, form):
        if self.is_popup():
            self.object = form.save()
            req = self.request
            tmpl = 'kanisa/members/services/composer_popup_close.html'
            return render_to_response(tmpl,
                                      {'object': self.object},
                                      context_instance=RequestContext(req))

        rval = super(KanisaCreateView, self).form_valid(form)

        messages.success(self.request, self.get_message(form.instance))

        return rval

composer_create = ComposerCreateView.as_view()
