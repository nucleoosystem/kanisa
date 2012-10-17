import urlparse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from kanisa.forms.auth import KanisaLoginForm


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
