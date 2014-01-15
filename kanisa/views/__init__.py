from django.conf import settings
from django.http import HttpResponseServerError
from django.template import Context, loader
from django.views.generic.base import TemplateView

from kanisa.models.banners import Banner


class KanisaIndexView(TemplateView):
    template_name = 'kanisa/public/homepage/index.html'

    def get_context_data(self, **kwargs):
        return {'banners': Banner.active_objects.all()}


def server_error(request, template_name='500.html'):
    tmpl = loader.get_template(template_name)

    context = Context(
        {
            'STATIC_URL': settings.STATIC_URL,
        }
    )

    return HttpResponseServerError(tmpl.render(context))
