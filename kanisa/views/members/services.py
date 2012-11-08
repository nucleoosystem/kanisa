from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.utils import formats
from django.views.generic.base import View
from kanisa.forms.services import AddSongToServiceForm
from kanisa.models import Service, SongInService
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import (KanisaListView,
                                  KanisaDetailView,
                                  KanisaFormView)


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

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.object.event.date,
                                             "DATE_FORMAT")
        title = 'Plan for %s (%s)' % (self.object.event.title,
                                      formatted_date)
        return title
service_detail = ServiceDetailView.as_view()


class BaseServiceManagementView(MembersBaseView):
    @property
    def service(self):
        if hasattr(self, "service_"):
            return self.service_

        self.service_ = get_object_or_404(Service,
                                          pk=int(self.kwargs['service_pk']))

        return self.service_


class AddSongView(BaseServiceManagementView, KanisaFormView):
    form_class = AddSongToServiceForm
    template_name = 'kanisa/members/form.html'

    def form_valid(self, form):
        # This code has a race condition that I just don't care about
        # very much.
        qs = SongInService.objects.filter(service=self.service)
        order = qs.aggregate(Max('order'))['order__max']

        if order is None:
            order = 0

        order += 1

        sis = SongInService.objects.create(song=form.cleaned_data['song'],
                                           service=self.service,
                                           order=order)
        self.service.songinservice_set.add(sis)

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


class MoveSongDownView(BaseServiceManagementView, View):
    def post(self, request, *args, **kwargs):
        songs = self.service.songinservice_set.all()

        pks = [song.pk for song in songs]

        i = pks.index(int(self.kwargs['song_pk']))

        if i == len(songs) - 1:
            raise Http404("That song can't move down.")

        songs[i].order, songs[i + 1].order = songs[i + 1].order, songs[i].order
        songs[i].save()
        songs[i + 1].save()

        return HttpResponseRedirect(reverse('kanisa_members_services_detail',
                                            args=[self.service.pk, ]))
move_down = MoveSongDownView.as_view()


class MoveSongUpView(BaseServiceManagementView, View):
    def post(self, request, *args, **kwargs):
        songs = self.service.songinservice_set.all()

        pks = [song.pk for song in songs]

        i = pks.index(int(self.kwargs['song_pk']))

        if i == 0:
            raise Http404("That song can't move up.")

        songs[i].order, songs[i - 1].order = songs[i - 1].order, songs[i].order
        songs[i].save()
        songs[i - 1].save()

        return HttpResponseRedirect(reverse('kanisa_members_services_detail',
                                            args=[self.service.pk, ]))
move_up = MoveSongUpView.as_view()
