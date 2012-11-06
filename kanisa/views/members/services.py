from kanisa.models import Service
from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaListView


class MembersServicesView(MembersBaseView, KanisaListView):
    template_name = 'kanisa/members/services/index.html'
    kanisa_title = 'Service Planning'

    def get_queryset(self):
        show_all_arg = self.request.GET.get('all', 0)
        show_all = show_all_arg == '1'
        if show_all:
            return Service.objects.all()
        else:
            return Service.future_objects.all()

index = MembersServicesView.as_view()
