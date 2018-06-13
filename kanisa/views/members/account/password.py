from django.contrib.auth.views import password_change
from django.contrib.sites.requests import RequestSite
from django.core import signing
from django.core.urlresolvers import reverse_lazy, reverse
from kanisa.forms.auth import (
    KanisaChangePasswordForm,
    KanisaPasswordRecoveryForm,
    KanisaPasswordResetForm
)
from kanisa.utils.mail import send_single_mail
from kanisa.views.generic import (
    KanisaTemplateView,
)
from password_reset.views import Recover, RecoverDone, Reset


def kanisa_members_password_change(request):
    return password_change(
        request,
        template_name='kanisa/management/password_reset.html',
        post_change_redirect='/members/',
        password_change_form=KanisaChangePasswordForm
    )


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
