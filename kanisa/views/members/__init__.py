from django.views.generic.base import TemplateView
from kanisa.views.generic import KanisaAuthorizationMixin


class MembersIndexView(KanisaAuthorizationMixin, TemplateView):
    template_name = 'kanisa/members/index.html'

    def authorization_check(self, user):
        return user.is_active
index = MembersIndexView.as_view()
