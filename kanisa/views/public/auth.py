import urlparse
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.models import Permission, User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.template import Context
from django.views.generic.edit import FormView, CreateView
from kanisa import conf
from kanisa.forms.auth import (KanisaLoginForm,
                               KanisaUserCreationForm)
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

        template_root = 'kanisa/emails/accountregistration/contents'
        plaintext_email = get_template('%s.txt' % template_root)
        html_email = get_template('%s.html' % template_root)

        d = Context({'user': form.instance,
                     'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

        subject = ('Registration for %s Pending Approval'
                   % form.instance.username)

        plaintext_content = plaintext_email.render(d)
        html_content = html_email.render(d)

        perm = Permission.objects.get(codename='manage_users')
        cond = Q(groups__permissions=perm) | Q(user_permissions=perm)
        users = User.objects.filter(cond).distinct().filter(is_active=True)

        for u in users:
            msg = EmailMultiAlternatives(subject,
                                         plaintext_content,
                                         conf.KANISA_FROM_EMAIL,
                                         [u.email, ])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

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
