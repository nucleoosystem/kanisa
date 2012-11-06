from django.views.generic.base import TemplateView
from kanisa.views.members.auth import MembersBaseView


class MembersIndexView(MembersBaseView, TemplateView):
    template_name = 'kanisa/members/index.html'
index = MembersIndexView.as_view()
