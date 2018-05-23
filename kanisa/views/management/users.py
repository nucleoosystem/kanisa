from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.models import RequestSite
from django.core.cache import cache
from django.db.models import Q
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from kanisa.forms.user import (
    UserCreateForm,
    UserUpdateForm,
)
from kanisa.models import RegisteredUser
from kanisa.utils.auth import users_with_perm
from kanisa.utils.mail import (
    send_bulk_mail,
    send_single_mail
)
from kanisa.views.generic import (
    KanisaAuthorizationMixin,
    KanisaDetailView,
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
    paginate_by = 20

    def get_filter_query(self):
        return self.request.GET.get('query')

    def get_queryset(self):
        query = self.get_filter_query()

        qs = get_user_model().objects.exclude(is_spam=True)
        qs = qs.order_by('is_active', 'username')

        if not query:
            return qs

        params = (Q(username__contains=query) |
                  Q(email__contains=query) |
                  Q(first_name__contains=query) |
                  Q(last_name__contains=query))

        qs = qs.filter(params)
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserManagementView,
                        self).get_context_data(**kwargs)
        context['query'] = self.get_filter_query()
        return context
user_management = UserManagementView.as_view()


class UserDetailView(UserBaseView,
                     KanisaDetailView):
    model = RegisteredUser
    template_name = 'kanisa/management/users/user_detail.html'
user_details = UserDetailView.as_view()


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

        send_bulk_mail(users_with_perm('manage_users'),
                       'on_account_activation_staff_notify',
                       {'user': user})

        user.is_active = True
        user.is_spam = False
        user.save()

        message = ('%s\'s account is now activated.'
                   % user.get_familiar_name())
        messages.success(self.request, message)

        cache.delete('kanisa_inactive_users')

        return reverse('kanisa_manage_users')
user_activate = UserActivateView.as_view()


class UserMarkSpamView(UserBaseView,
                       RedirectView):
    permanent = False

    def get_redirect_url(self, user_id):
        user = get_object_or_404(get_user_model(), pk=user_id)

        send_bulk_mail(users_with_perm('manage_users'),
                       'on_account_spam_staff_notify',
                       {'user': user})

        user.is_active = False
        user.is_spam = True
        user.save()

        message = ('%s\'s account has been marked as spam.'
                   % user.get_familiar_name())
        messages.success(self.request, message)

        cache.delete('kanisa_inactive_users')

        return reverse('kanisa_manage_users')
user_spam = UserMarkSpamView.as_view()


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


class UserCreateView(UserBaseView,
                     KanisaFormView):
    form_class = UserCreateForm
    success_url = reverse_lazy('kanisa_manage_users')
    template_name = 'kanisa/management/create.html'
    kanisa_title = 'Create User'

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']

        if not form.cleaned_data['image']:
            # Comes in as False, need to set to None
            image = None
        else:
            image = form.cleaned_data['image']

        if self.request.user.is_superuser:
            is_superuser = form.cleaned_data['administrator']
            is_staff = form.cleaned_data['administrator']
        else:
            is_superuser = False
            is_staff = False

        object = RegisteredUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            image=image,
            is_superuser=is_superuser,
            is_staff=is_staff
        )

        object.set_kanisa_permissions(form.cleaned_data['permissions'])

        password = RegisteredUser.objects.make_random_password()
        object.set_password(password)

        object.save()

        send_single_mail(object,
                         'on_account_creation',
                         {'password': password,
                          'site': RequestSite(self.request), })

        message = ('Registered User "%s" saved.'
                   % object.get_familiar_name())
        messages.success(self.request, message)

        return super(UserCreateView, self).form_valid(form)
user_create = UserCreateView.as_view()
