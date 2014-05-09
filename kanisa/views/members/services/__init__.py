from django.core.urlresolvers import reverse_lazy
from django.utils import formats
from kanisa.models import (
    Band,
    Service,
    Song,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
    KanisaDetailView
)


class ServiceBaseView(KanisaAuthorizationMixin):
    kanisa_root_crumb = {
        'text': 'Services',
        'url': reverse_lazy('kanisa_members_services_index')
    }

    def authorization_check(self, user):
        if not user.is_active:
            return False

        return user.can_see_service_plans()


class ServiceRestrictedBaseView(KanisaAuthorizationMixin):
    kanisa_root_crumb = {'text': 'Services',
                         'url': reverse_lazy('kanisa_members_services_index')}
    permission = 'kanisa.manage_services'


class ServiceIndexView(ServiceBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
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
        context['bands'] = Band.objects.all()

        musician_services = self.request.user.service_musicians.all()
        leader_services = self.request.user.service_set.all()

        all_service_pks = set(
            [s.pk for s in musician_services] +
            [s.pk for s in leader_services]
        )

        for service in context['service_list']:
            service.user_is_involved = service.pk in all_service_pks

        active = [s.user_is_involved for s in context['service_list']]
        context['active_in_some_services'] = any(active)

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
