from kanisa.views.members.auth import MembersBaseView
from kanisa.views.generic import KanisaTemplateView


class MembersServicesView(MembersBaseView, KanisaTemplateView):
    template_name = 'kanisa/members/services/index.html'
    kanisa_title = 'Service Planning'
index = MembersServicesView.as_view()
