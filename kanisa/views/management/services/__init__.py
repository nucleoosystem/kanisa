from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Count, Max
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils import formats
from django.views.generic.base import View
from kanisa.forms.services import (
    AddSongToServiceForm,
    BandForm,
    ComposerForm,
    CreateSongForm,
    ServiceForm,
)
from kanisa.models import (
    Band,
    Service,
    Song,
    SongInService,
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaDeleteView,
    KanisaDetailView,
    KanisaFormView,
    KanisaListView,
    KanisaUpdateView,
)


class ServiceBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having service planning on your site helps your service '
                   'leaders co-ordinate.')
    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_manage_services')}
    permission = 'kanisa.manage_services'
    kanisa_nav_component = 'services'


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/management/services/index.html'
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

        songs = Song.objects.all()
        songs = songs.annotate(usage=Count('songinservice'))
        songs = songs.order_by('-usage')

        context['top_five_songs'] = songs[:5]
        context['bands'] = Band.objects.all()

        return context
service_management = ServiceIndexView.as_view()


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


class ServiceDetailView(ServiceBaseView, KanisaDetailView):
    model = Service
    pk_url_kwarg = 'service_pk'
    template_name = 'kanisa/management/services/service_detail.html'

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


class ServiceCreateView(ServiceBaseView,
                        KanisaCreateView):
    form_class = ServiceForm
    kanisa_title = 'Create a Service Plan'

    def get_success_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.object.pk, ])
service_create = ServiceCreateView.as_view()


class BaseServiceManagementView(ServiceBaseView):
    @property
    def service(self):
        if not hasattr(self, "service_"):
            pk = int(self.kwargs['service_pk'])
            self.service_ = get_object_or_404(Service, pk=pk)

        return self.service_


class ServiceUpdateView(BaseServiceManagementView,
                        KanisaUpdateView):
    form_class = ServiceForm
    model = Service
    pk_url_kwarg = 'service_pk'

    def get_success_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.service.pk, ])
service_update = ServiceUpdateView.as_view()


class ServiceDeleteView(BaseServiceManagementView,
                        KanisaDeleteView):
    model = Service
    pk_url_kwarg = 'service_pk'

    def get_cancel_url(self):
        return reverse('kanisa_manage_services_detail',
                       args=[self.service.pk, ])

    def get_success_url(self):
        return reverse('kanisa_manage_services')
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
