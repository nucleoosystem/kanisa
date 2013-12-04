from django.core.urlresolvers import reverse_lazy
from django.utils import formats
from kanisa.models import (
    Service,
    Song,
)
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import (
    KanisaListView,
    KanisaDetailView,
)


class ServiceBaseView(MembersBaseView):
    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_members_services_index')}


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
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
        return context
index = ServiceIndexView.as_view()


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
