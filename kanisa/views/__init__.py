import urlparse

from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView
from haystack.query import SearchQuerySet

from kanisa.forms.auth import KanisaLoginForm, KanisaUserCreationForm
from kanisa.models.banners import Banner
from kanisa.views.generic import (KanisaAnyAuthorizationMixin,
                                  KanisaTemplateView)


class KanisaIndexView(TemplateView):
    template_name = 'kanisa/public/index.html'

    def get_context_data(self, **kwargs):
        return {'banners': Banner.active_objects.all()}


class KanisaManagementIndexView(KanisaAnyAuthorizationMixin,
                                KanisaTemplateView):
    template_name = 'kanisa/management/index.html'


class KanisaLoginView(FormView):
    template_name = 'kanisa/login.html'
    form_class = KanisaLoginForm
    success_url = reverse_lazy('kanisa_manage_index')

    def form_valid(self, form):
        redirect_to = self.request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        netloc = urlparse.urlparse(redirect_to)[1]

        # Use default setting if redirect_to is empty
        if not redirect_to:
            redirect_to = self.success_url

        # Heavier security check -- don't allow redirection to a
        # different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = self.success_url

        # Okay, security checks complete. Log the user in.
        login(self.request, form.get_user())
        return HttpResponseRedirect(redirect_to)


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


class KanisaRegistrationView(CreateView):
    template_name = 'kanisa/registration.html'
    form_class = KanisaUserCreationForm
    success_url = reverse_lazy('kanisa_public_registration_thanks')

    def form_valid(self, form):
        rval = super(KanisaRegistrationView, self).form_valid(form)

        return rval


class KanisaRegistrationThanksView(KanisaTemplateView):
    kanisa_title = 'Registration Complete'
    template_name = 'kanisa/registration_thanks.html'
