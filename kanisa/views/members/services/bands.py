from django.core.urlresolvers import reverse_lazy
from kanisa.forms.services import BandForm
from kanisa.models import Band
from kanisa.views.generic import (
    KanisaCreateView,
    KanisaDeleteView,
    KanisaUpdateView,
)
from kanisa.views.members.services import ServiceRestrictedBaseView


class BandCreateView(ServiceRestrictedBaseView,
                     KanisaCreateView):
    form_class = BandForm
    kanisa_title = 'Add a Band'
    success_url = reverse_lazy('kanisa_members_services_index')

    def get_template_names(self):
        return ['kanisa/members/form.html', ]
band_create = BandCreateView.as_view()


class BandUpdateView(ServiceRestrictedBaseView,
                     KanisaUpdateView):
    model = Band
    form_class = BandForm
    success_url = reverse_lazy('kanisa_members_services_index')

    def get_template_names(self):
        return ['kanisa/members/form.html', ]
band_update = BandUpdateView.as_view()


class RemoveBandView(ServiceRestrictedBaseView,
                     KanisaDeleteView):
    model = Band
    success_url = reverse_lazy('kanisa_members_services_index')

    def get_cancel_url(self):
        return self.success_url

    def get_template_names(self):
        return ['kanisa/members/delete.html', ]
remove_band = RemoveBandView.as_view()
