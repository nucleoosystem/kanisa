from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet

from kanisa.models.banners import Banner
from kanisa.views.generic import KanisaTemplateView


def index(request):
    banners = Banner.active_objects.all()

    return render_to_response('kanisa/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


@staff_member_required
def manage(request):
    return render_to_response('kanisa/management/index.html',
                              {},
                              context_instance=RequestContext(request))


class KanisaSearchView(KanisaTemplateView):
    kanisa_title = 'Search'
    template_name = 'kanisa/management/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)

        context = self.get_context_data(**kwargs)

        if query:
            context['search_term'] = query
            matching = SearchQuerySet().filter(content=request.GET['query'])
            context['results'] = matching

        return render_to_response(self.template_name,
                                  context,
                                  context_instance=RequestContext(request))
