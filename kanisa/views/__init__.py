from django.views.generic.base import TemplateView

from kanisa.models.banners import Banner
from kanisa.views.generic import (KanisaAnyAuthorizationMixin,
                                  KanisaTemplateView)


class KanisaIndexView(TemplateView):
    template_name = 'kanisa/public/homepage/index.html'

    def get_context_data(self, **kwargs):
        return {'banners': Banner.active_objects.all()}


class KanisaManagementIndexView(KanisaAnyAuthorizationMixin,
                                KanisaTemplateView):
    template_name = 'kanisa/management/index.html'
