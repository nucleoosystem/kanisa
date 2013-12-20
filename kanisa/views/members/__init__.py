from django.views.generic.base import TemplateView
from kanisa.models import Document, Service
from kanisa.views.members.auth import MembersBaseView


class MembersIndexView(MembersBaseView, TemplateView):
    template_name = 'kanisa/members/index.html'

    def get_context_data(self, **kwargs):
        context = super(MembersIndexView,
                        self).get_context_data(**kwargs)

        context['documents'] = Document.objects.all()[:5]

        if self.request.user.can_see_service_plans():
            context['services'] = Service.future_objects.all()[:5]
        else:
            context['services'] = None

        return context
index = MembersIndexView.as_view()
