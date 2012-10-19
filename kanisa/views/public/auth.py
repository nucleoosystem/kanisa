import urlparse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.template import Context
from django.views.generic.edit import FormView, CreateView
from kanisa import conf
from kanisa.forms.auth import (KanisaLoginForm,
                               KanisaUserCreationForm)
from kanisa.utils.auth import users_with_perm
from kanisa.utils.mail import send_bulk_mail
from kanisa.views.generic import KanisaTemplateView


class KanisaLoginView(FormView):
    template_name = 'kanisa/auth/login.html'
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


class KanisaRegistrationView(CreateView):
    template_name = 'kanisa/auth/registration.html'
    form_class = KanisaUserCreationForm
    success_url = reverse_lazy('kanisa_public_registration_thanks')

    def form_valid(self, form):
        rval = super(KanisaRegistrationView, self).form_valid(form)

        cache.delete('kanisa_inactive_users')

        subject = ('Registration for %s Pending Approval'
                   % form.instance.username)
        template = 'accountregistration'
        context = Context({'user': form.instance,
                           'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

        users = users_with_perm('manage_users')

        send_bulk_mail(users, subject, template, context)

        return rval

    def get_context_data(self, *args, **kwargs):
        if not conf.KANISA_REGISTRATION_ALLOWED:
            raise Http404

        return super(KanisaRegistrationView,
                     self).get_context_data(*args, **kwargs)


class KanisaRegistrationThanksView(KanisaTemplateView):
    kanisa_title = 'Registration Complete'
    template_name = 'kanisa/auth/registration_thanks.html'

    def get_context_data(self, *args, **kwargs):
        if not conf.KANISA_REGISTRATION_ALLOWED:
            raise Http404

        return super(KanisaRegistrationThanksView,
                     self).get_context_data(*args, **kwargs)
