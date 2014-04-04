import urlparse
from django.contrib.auth import (
    get_user_model,
    login,
    REDIRECT_FIELD_NAME
)
from django.contrib.sites.models import RequestSite
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView, CreateView
from kanisa import conf
from kanisa.forms.auth import (
    KanisaAccountModificationForm,
    KanisaLoginForm,
    KanisaAccountCreationForm,
)
from kanisa.utils.auth import has_any_kanisa_permission, users_with_perm
from kanisa.utils.mail import send_bulk_mail
from kanisa.views.generic import (
    KanisaTemplateView,
    KanisaUpdateView
)
from kanisa.views.members.auth import MembersBaseView


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
                       {'user': form.instance,
                        'site': RequestSite(self.request), })

        return rval


class KanisaRegistrationThanksView(KanisaRegistrationMixin,
                                   KanisaTemplateView):
    kanisa_title = 'Registration Complete'
    template_name = 'kanisa/auth/registration_thanks.html'
