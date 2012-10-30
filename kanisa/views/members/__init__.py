from django.views.generic.base import TemplateView
from kanisa.views.generic import KanisaAuthorizationMixin


class MembersBaseView(KanisaAuthorizationMixin):
    def authorization_check(self, user):
        return user.is_active


class MembersIndexView(MembersBaseView, TemplateView):
    template_name = 'kanisa/members/index.html'
index = MembersIndexView.as_view()
