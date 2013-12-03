from django.core.urlresolvers import reverse_lazy
from django.db.models import Count
from kanisa.models import (
    Band,
    Service,
    Song,
    SongInService,
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
)


class ServiceBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Having service planning on your site helps your service '
                   'leaders co-ordinate service plans.')
    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_manage_services')}
    permission = 'kanisa.manage_services'
    kanisa_nav_component = 'services'


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/management/services/index.html'
    kanisa_title = 'Service Planning'
    kanisa_is_root_view = True

    def get_queryset(self):
        if self.kwargs['show_all']:
            return Service.objects.all()
        else:
            return Service.future_objects.all()

    def get_context_data(self, **kwargs):
        context = super(ServiceIndexView,
                        self).get_context_data(**kwargs)
        context['showing_all'] = self.kwargs['show_all']

        songs = Song.objects.all()
        songs = songs.annotate(usage=Count('songinservice'))
        songs = songs.order_by('-usage')
        songs = songs[:5]

        total_songs = SongInService.objects.count()

        if total_songs == 0:
            percents = [0 for s in songs]
        else:
            percents = [(s.usage * 100.0) / total_songs for s in songs]

        context['top_five_songs'] = zip(songs, percents)
        context['bands'] = Band.objects.all()

        return context
service_management = ServiceIndexView.as_view()
