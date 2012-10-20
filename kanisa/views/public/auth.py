import urlparse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.sites.models import RequestSite
from django.core import signing
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView, CreateView
from kanisa import conf
from kanisa.forms.auth import (KanisaLoginForm,
                               KanisaUserCreationForm,
                               KanisaPasswordRecoveryForm,
                               KanisaPasswordResetForm)
from kanisa.utils.auth import users_with_perm
from kanisa.utils.mail import send_bulk_mail, send_single_mail
from kanisa.views.generic import KanisaTemplateView
from password_reset.views import Recover, Reset


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


class KanisaRegistrationMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not conf.KANISA_REGISTRATION_ALLOWED:
            raise Http404

        return super(KanisaRegistrationMixin,
                     self).dispatch(request, *args, **kwargs)


class KanisaRegistrationView(KanisaRegistrationMixin, CreateView):
    template_name = 'kanisa/auth/registration.html'
    form_class = KanisaUserCreationForm
    success_url = reverse_lazy('kanisa_public_registration_thanks')

    def form_valid(self, form):
        rval = super(KanisaRegistrationView, self).form_valid(form)

        cache.delete('kanisa_inactive_users')

        send_bulk_mail(users_with_perm('manage_users'),
                       'on_account_registration',
                       {'user': form.instance})

        return rval


class KanisaRegistrationThanksView(KanisaRegistrationMixin,
                                   KanisaTemplateView):
    kanisa_title = 'Registration Complete'
    template_name = 'kanisa/auth/registration_thanks.html'


class KanisaRecoverPasswordView(Recover):
    template_name = 'kanisa/auth/passwordreset/recovery_form.html'
    form_class = KanisaPasswordRecoveryForm

    def send_notification(self):
        context = {
            'site': RequestSite(self.request),
            'user': self.user,
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }

        send_single_mail(self.user,
                         'on_forgotten_password',
                         context)

class KanisaResetPasswordView(Reset):
    template_name = 'kanisa/auth/passwordreset/reset_form.html'
    form_class = KanisaPasswordResetForm
    success_url = reverse_lazy('kanisa_public_password_reset_done')


class KanisaResetPasswordDoneView(KanisaTemplateView):
    kanisa_title = 'Password Reset Complete'
    template_name = 'kanisa/auth/passwordreset/reset_done.html'
