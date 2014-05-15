from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from kanisa.models import (
    Band,
    Service,
)
from kanisa.utils.services import most_popular_songs
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
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


class BaseServiceManagementView(ServiceRestrictedBaseView):
    @property
    def service(self):
        if not hasattr(self, "service_"):
            pk = int(self.kwargs['service_pk'])
            self.service_ = get_object_or_404(Service, pk=pk)

        return self.service_
