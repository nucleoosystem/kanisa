from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
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
