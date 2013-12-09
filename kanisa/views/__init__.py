from django.views.generic.base import TemplateView

from kanisa.models.banners import Banner


class KanisaIndexView(TemplateView):
    template_name = 'kanisa/public/homepage/index.html'

    def get_context_data(self, **kwargs):
        return {'banners': Banner.active_objects.all()}
