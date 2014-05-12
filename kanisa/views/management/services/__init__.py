from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import formats
from kanisa.forms.services import (
    ServiceForm,
)
from kanisa.models import (
    Service,
    Song,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaCreateView,
    KanisaDeleteView,
    KanisaDetailView,
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
        context['top_five_songs'] = most_popular_songs()[:5]

        return context
service_management = ServiceIndexView.as_view()


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
