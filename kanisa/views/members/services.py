from django.shortcuts import get_object_or_404
from django.utils import formats
from kanisa.forms.services import AddSongToServiceForm
from kanisa.models import Service
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
    template_name = 'kanisa/members/services/service_detail.html'

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.object.event.date,
                                             "DATE_FORMAT")
        title = 'Plan for %s (%s)' % (self.object.event.title,
                                      formatted_date)
        return title
service_detail = ServiceDetailView.as_view()


class AddSongView(MembersBaseView, KanisaFormView):
    form_class = AddSongToServiceForm
    template_name = 'kanisa/members/form.html'

    @property
    def service(self):
        if hasattr(self, "service_"):
            return self.service_

        self.service_ = get_object_or_404(Service,
                                          pk=int(self.kwargs['pk']))

        return self.service_

    def get_success_url(self):
        return '/'

    def get_kanisa_title(self):
        formatted_date = formats.date_format(self.service.event.date,
                                             "DATE_FORMAT")
        return 'Add a song to %s (%s)' % (self.service.event.title,
                                          formatted_date)

add_song = AddSongView.as_view()
