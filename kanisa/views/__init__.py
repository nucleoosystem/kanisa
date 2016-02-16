from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import HttpResponseServerError
from django.template import Context, loader
from django.views.generic.base import TemplateView

from kanisa.models import Banner, BlogPost, SiteWideNotice


class KanisaIndexView(TemplateView):
    template_name = 'kanisa/public/homepage/index.html'

    def get_notice(self):
        if 'preview_notice' in self.request.GET:
            try:
                return SiteWideNotice.objects.get(
                    pk=self.request.GET['preview_notice']
                )
            except SiteWideNotice.DoesNotExist:
                pass

        notices = SiteWideNotice.active_objects.all()[:1]

        if not notices:
            return None

        return notices[0]

    def get_context_data(self, **kwargs):
        cutoff = date.today() - relativedelta(months=2)
        blogposts = BlogPost.published_objects.filter(
            publish_date__gte=cutoff
        )[:2]

        return {
            'banners': Banner.active_objects.all(),
            'blogposts': blogposts,
            'notice': self.get_notice()
        }


def server_error(request, template_name='500.html'):
    tmpl = loader.get_template(template_name)

    context = Context(
        {
            'STATIC_URL': settings.STATIC_URL,
        }
    )

    return HttpResponseServerError(tmpl.render(context))
