import urlparse

from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.edit import FormView
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
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


class KanisaLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        css = "btn-primary btn-large btn-success"
        submit_text = 'Login'
        self.helper.add_input(Submit('submit',
                                     submit_text,
                                     css_class=css))

        super(KanisaLoginForm, self).__init__(*args, **kwargs)


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
