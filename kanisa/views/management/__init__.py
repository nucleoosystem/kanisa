from kanisa.views.generic import (KanisaAnyAuthorizationMixin,
                                  KanisaTemplateView)


class KanisaManagementIndexView(KanisaAnyAuthorizationMixin,
                                KanisaTemplateView):
    template_name = 'kanisa/management/index.html'
