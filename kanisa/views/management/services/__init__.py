from django.core.urlresolvers import reverse_lazy
from kanisa.models import Service
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
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
        context['top_five_songs'] = most_popular_songs()[:5]

        return context
service_management = ServiceIndexView.as_view()
