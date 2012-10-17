from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.query import SearchQuerySet

from kanisa.views.generic import KanisaTemplateView


class KanisaSearchView(KanisaTemplateView):
    kanisa_title = 'Search'
    template_name = 'kanisa/public/search.html'
    results_per_page = 10

    def slice_results(self, request, results):
        try:
            page_no = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404("Not a valid number for page.")

        if page_no < 1:
            raise Http404("Pages should be 1 or greater.")

        paginator = Paginator(results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)

        context = self.get_context_data(**kwargs)

        if query:
            context['search_term'] = query
            matching = SearchQuerySet().filter(content=request.GET['query'])
            paginator, page = self.slice_results(request, matching)

            context['page_obj'] = page

        return render_to_response(self.template_name,
                                  context,
                                  context_instance=RequestContext(request))
