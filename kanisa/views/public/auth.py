import urlparse
from django.contrib.auth import (
    get_user_model,
    login,
    REDIRECT_FIELD_NAME
)
from django.contrib.auth.views import password_change
from django.contrib.sites.models import RequestSite
from django.core import signing
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView, CreateView
from kanisa import conf
from kanisa.forms.auth import (
    KanisaAccountModificationForm,
    KanisaChangePasswordForm,
    KanisaLoginForm,
    KanisaAccountCreationForm,
    KanisaPasswordRecoveryForm,
    KanisaPasswordResetForm
)
from kanisa.utils.auth import has_any_kanisa_permission, users_with_perm
from kanisa.utils.mail import send_bulk_mail, send_single_mail
from kanisa.views.generic import (
    KanisaTemplateView,
    KanisaUpdateView
)
from kanisa.views.members.auth import MembersBaseView
from password_reset.views import Recover, RecoverDone, Reset


def kanisa_members_password_change(request):
    return password_change(
        request,
        template_name='kanisa/management/password_reset.html',
        post_change_redirect='/members/',
        password_change_form=KanisaChangePasswordForm
    )


class KanisaLoginView(FormView):
    template_name = 'kanisa/auth/login.html'
    form_class = KanisaLoginForm
    success_url = reverse_lazy('kanisa_manage_index')

    def get_success_url(self, user):
        if has_any_kanisa_permission(user):
            return self.success_url

        return reverse('kanisa_members_index')

    def form_valid(self, form):
        redirect_to = self.request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        netloc = urlparse.urlparse(redirect_to)[1]

        # Use default setting if redirect_to is empty
        if not redirect_to:
            redirect_to = self.get_success_url(form.get_user())

        # Heavier security check -- don't allow redirection to a
        # different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = self.get_success_url(form.get_user())

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
    form_class = KanisaAccountCreationForm
    success_url = reverse_lazy('kanisa_members_registration_thanks')

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

    def get_success_url(self):
        return reverse('kanisa_members_reset_password_sent',
                       args=[self.mail_signature, ])

    def send_notification(self):
        context = {
            'site': RequestSite(self.request),
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }

        send_single_mail(self.user,
                         'on_forgotten_password',
                         context)


class KanisaResetPasswordView(Reset):
    template_name = 'kanisa/auth/passwordreset/reset_form.html'
    form_class = KanisaPasswordResetForm
    success_url = reverse_lazy('kanisa_members_reset_password_done')


class KanisaResetPasswordSentView(KanisaTemplateView, RecoverDone):
    kanisa_title = 'Password Reset Email Sent'
    template_name = 'kanisa/auth/passwordreset/recovery_mail_sent.html'


class KanisaResetPasswordDoneView(KanisaTemplateView):
    kanisa_title = 'Password Reset Complete'
    template_name = 'kanisa/auth/passwordreset/reset_done.html'


class KanisaAccountModificationView(MembersBaseView,
                                    KanisaUpdateView):
    template_name = 'kanisa/auth/account.html'
    form_class = KanisaAccountModificationForm
    success_url = reverse_lazy('kanisa_members_index')
    model = get_user_model()
    kanisa_title = 'Update your account'

    def get_object(self):
        return self.request.user

    def get_message(self, form):
        return 'Changes saved.'
