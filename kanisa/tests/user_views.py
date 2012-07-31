from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.loader import render_to_string
from kanisa.tests.utils import KanisaViewTestCase


class UserManagementViewTest(KanisaViewTestCase):

    def setUp(self):
        if hasattr(self, 'setup_called'):
            return

        super(UserManagementViewTest, self).setUp()

        p = Permission.objects.get(codename='manage_users')
        fred = User.objects.get(username='fred')
        fred.user_permissions.add(p)
        fred.save()

    def test_views_protected(self):
        self.view_is_restricted(reverse('kanisa_manage_users'))

    def test_base_view(self):
        self.client.login(username='fred', password='secret')
        resp = self.client.get(reverse('kanisa_manage_users'))
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('user_list' in resp.context)

        bob = User.objects.get(username='bob')
        fred = User.objects.get(username='fred')

        self.assertEqual(list(resp.context['user_list']),
                         [bob, fred, ])

        self.client.logout()

    def test_template_complexity(self):
        tmpl = 'kanisa/management/users/_user_list.html'
        users = list(User.objects.all())
        with self.assertNumQueries(16):
            render_to_string(tmpl,
                             {'user_list': users})

    def test_template_tags(self):
        def check_perm_template(user, perm):
            template = ("{%% load kanisa_tags %%}"
                        "{%% kanisa_user_has_perm '%s' %%}" % perm)
            t = Template(template)
            c = Context({"theuser": user})
            return t.render(c)

        bob = User.objects.get(username='bob')
        fred = User.objects.get(username='fred')

        # Fred has access to manage users, not to manage social
        # networks.
        with self.assertNumQueries(4):
            output = check_perm_template(fred, 'kanisa.manage_users')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'checked="checked" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_users" '
                                  'data-user-id="2" '
                                  'title="Can manage your users" '
                                  '/>'))
            output = check_perm_template(fred, 'kanisa.manage_social')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_social" '
                                  'data-user-id="2" '
                                  'title="Can manage your social networks" '
                                  '/>'))

        # Bob doesn't have access to either
        with self.assertNumQueries(4):
            output = check_perm_template(bob, 'kanisa.manage_users')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_users" '
                                  'data-user-id="1" '
                                  'title="Can manage your users" '
                                  '/>'))
            output = check_perm_template(bob, 'kanisa.manage_social')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_social" '
                                  'data-user-id="1" '
                                  'title="Can manage your social networks" '
                                  '/>'))
