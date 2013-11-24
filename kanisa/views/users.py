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
    KanisaFormView,
    KanisaListView
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

        send_single_mail(user, 'on_account_activation', {})

        user.is_active = True
        user.save()

        message = ('%s\'s account is now activated.'
                   % user.get_familiar_name())
        messages.success(self.request, message)

        cache.delete('kanisa_inactive_users')

        return reverse('kanisa_manage_users')
user_activate = UserActivateView.as_view()


class UserUpdateView(UserBaseView,
                     KanisaFormView):
    form_class = UserUpdateForm
    success_url = reverse_lazy('kanisa_manage_users')
    template_name = 'kanisa/management/create.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(RegisteredUser, pk=kwargs['pk'])
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'email': self.object.email,
            'image': self.object.image,
            'permissions': [p.codename
                            for p in self.object.get_kanisa_permissions()],
        }

        if self.request.user.is_superuser:
            initial['administrator'] = self.object.is_superuser

        return initial

    def get_kanisa_title(self):
        return 'Edit User: %s' % self.object.get_display_name()

    def get_form_kwargs(self):
        kwargs = super(UserUpdateView, self).get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object.first_name = form.cleaned_data['first_name']
        self.object.last_name = form.cleaned_data['last_name']
        self.object.email = form.cleaned_data['email']

        if not form.cleaned_data['image']:
            # Comes in as False, need to set to None
            self.object.image = None
        else:
            self.object.image = form.cleaned_data['image']

        if self.request.user.is_superuser:
            self.object.is_superuser = form.cleaned_data['administrator']
            self.object.is_staff = form.cleaned_data['administrator']

        self.object.set_kanisa_permissions(form.cleaned_data['permissions'])

        self.object.save()

        message = ('Registered User "%s" saved.'
                   % self.object.get_familiar_name())
        messages.success(self.request, message)

        return super(UserUpdateView, self).form_valid(form)
user_update = UserUpdateView.as_view()
