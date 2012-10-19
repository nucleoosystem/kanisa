from django.contrib import messages
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.template import Context
from django.views.generic.base import RedirectView
from kanisa import conf
from kanisa.utils.mail import send_single_mail
from kanisa.views.generic import (KanisaAuthorizationMixin,
                                  KanisaListView)


class UserBaseView(KanisaAuthorizationMixin):
    kanisa_lead = ('Users are people authorised to see  and manage different'
                   ' parts of your site.')
    kanisa_root_crumb = {'text': 'Users',
                         'url': reverse_lazy('kanisa_manage_users')}
    permission = 'kanisa.manage_users'
    kanisa_nav_component = 'users'


class UserManagementView(UserBaseView,
                         KanisaListView):
    queryset = User.objects.all().order_by('username')
    template_name = 'kanisa/management/users/index.html'
    kanisa_title = 'Manage Users'
    kanisa_is_root_view = True


class UserActivateView(UserBaseView,
                       RedirectView):
    permanent = False

    def get_redirect_url(self, user_id):
        user = get_object_or_404(User, pk=user_id)

        if user.is_active:
            message = '%s\'s account is already active.' % unicode(user)
            messages.success(self.request, message)
            return reverse('kanisa_manage_users')

        subject = '%s Account Activated' % conf.KANISA_CHURCH_NAME
        template = 'accountactivation'
        context = Context({'user': user,
                           'KANISA_CHURCH_NAME': conf.KANISA_CHURCH_NAME})

        send_single_mail(user, subject, template, context)

        user.is_active = True
        user.save()

        message = '%s\'s account is now activated.' % unicode(user)
        messages.success(self.request, message)

        cache.delete('kanisa_inactive_users')

        return reverse('kanisa_manage_users')
