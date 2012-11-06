from kanisa.models import Service
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersServicesView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
    kanisa_title = 'Service Planning'

    def get_queryset(self):
        show_all_arg = self.request.GET.get('all', 0)
        self.show_all = show_all_arg == '1'

        if self.show_all:
            return Service.objects.all()
        else:
            return Service.future_objects.all()

    def get_context_data(self, **kwargs):
        context = super(MembersServicesView,
                        self).get_context_data(**kwargs)
        context['showing_all'] = self.show_all
        return context

index = MembersServicesView.as_view()
