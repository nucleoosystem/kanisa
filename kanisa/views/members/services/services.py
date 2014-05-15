from django.core.urlresolvers import reverse
from django.utils import formats
from kanisa.forms.services import ServiceForm
from kanisa.models import (
    Service,
    Song,
)
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaDeleteView,
    KanisaDetailView,
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
