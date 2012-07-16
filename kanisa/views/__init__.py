from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet

from kanisa.models.banners import Banner
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaTemplateView)


def index(request):
    banners = Banner.active_objects.all()

    return render_to_response('kanisa/index.html',
                              {'banners': banners},
                              context_instance=RequestContext(request))


class KanisaManagementIndexView(KanisaAuthorizationMixin,
                                KanisaTemplateView):
    template_name = 'kanisa/management/index.html'


class KanisaSearchView(KanisaAuthorizationMixin,
                       KanisaTemplateView):
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
