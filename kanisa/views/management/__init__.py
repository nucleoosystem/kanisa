from django.contrib.auth import get_user_model
from kanisa.views.generic import (KanisaAnyAuthorizationMixin,
                                  KanisaTemplateView)


class KanisaManagementIndexView(KanisaAnyAuthorizationMixin,
                                KanisaTemplateView):
    template_name = 'kanisa/management/index.html'

    def get_context_data(self, **kwargs):
        context = super(KanisaManagementIndexView,
                        self).get_context_data(**kwargs)

        users = get_user_model().objects.all()
        context['user_list'] = users.order_by('-last_login')[:5]

        return context
