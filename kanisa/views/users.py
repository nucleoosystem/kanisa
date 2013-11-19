from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms.user import UserUpdateForm
from kanisa.models import RegisteredUser
from kanisa.utils.mail import send_single_mail
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaListView,
    KanisaUpdateView
)


class UserBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Users are people authorised to see  and manage different'
                   ' parts of your site.')
    kanisa_root_crumb = {'text': 'Users',
                         'url': reverse_lazy('kanisa_manage_users')}
    permission = 'kanisa.manage_users'
    kanisa_nav_component = 'users'


class UserManagementView(UserBaseView,
                         KanisaListView):
    template_name = 'kanisa/management/users/index.html'
    kanisa_title = 'Manage Users'
    kanisa_is_root_view = True
    context_object_name = 'user_list'

    def get_queryset(self):
        return get_user_model().objects.all().order_by('username')
user_management = UserManagementView.as_view()


class UserActivateView(UserBaseView,
                       RedirectView):
    permanent = False

    def get_redirect_url(self, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)

        if user.is_active:
            message = ('%s\'s account is already active.'
                       % user.get_familiar_name())
            messages.success(self.request, message)
            return reverse('kanisa_manage_users')

        send_single_mail(user,
                         'on_account_activation',
                         {'user': user})

        user.is_active = True
        user.save()

        message = ('%s\'s account is now activated.'
                   % user.get_familiar_name())
        messages.success(self.request, message)

        cache.delete('kanisa_inactive_users')

        return reverse('kanisa_manage_users')
user_activate = UserActivateView.as_view()


class UserUpdateView(UserBaseView,
                     KanisaUpdateView):
    form_class = UserUpdateForm
    model = RegisteredUser
    success_url = reverse_lazy('kanisa_manage_users')
user_update = UserUpdateView.as_view()
