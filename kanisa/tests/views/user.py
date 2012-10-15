from django.contrib.auth.models import User, Permission
from django.contrib.auth.context_processors import PermWrapper
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.loader import render_to_string
from kanisa.tests.utils import KanisaViewTestCase


class UserManagementViewTest(KanisaViewTestCase):

    def setUp(self):
        super(UserManagementViewTest, self).setUp()

        p = Permission.objects.get(codename='manage_users')
        fred = User.objects.get(username='fred')
        fred.user_permissions.add(p)
        fred.save()

    def test_views_protected(self):
        self.view_is_restricted(reverse('kanisa_manage_users'))
        self.view_is_restricted(reverse('kanisa_manage_users_activate',
                                        args=[1, ]))

    def test_base_view(self):
        self.client.login(username='fred', password='secret')
        resp = self.client.get(reverse('kanisa_manage_users'))
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('user_list' in resp.context)

        bob = User.objects.get(username='bob')
        fred = User.objects.get(username='fred')
        superman = User.objects.get(username='superman')

        self.assertEqual(list(resp.context['user_list']),
                         [bob, fred, superman, ])

        self.client.logout()

    def test_template_complexity(self):
        tmpl = 'kanisa/management/users/_user_list.html'
        users = list(User.objects.all())
        user = User.objects.get(username='superman')
        perms = PermWrapper(user)

        with self.assertNumQueries(4):
            render_to_string(tmpl,
                             {'user_list': users,
                              'user': user,
                              'perms': perms})

    def test_template_tags(self):
        # To make sure this test is independent of other cached keys.
        cache.clear()

        def check_perm_template(request_user, user, perm):
            template = ("{%% load kanisa_tags %%}"
                        "{%% kanisa_user_has_perm '%s' %%}" % perm)
            t = Template(template)
            c = Context({"theuser": user, "user": request_user})
            return t.render(c)

        bob = User.objects.get(username='bob')
        fred = User.objects.get(username='fred')
        superman = User.objects.get(username='superman')

        # Fred has access to manage users, not to manage social
        # networks.
        with self.assertNumQueries(3):
            output = check_perm_template(superman, fred,
                                         'kanisa.manage_users')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'checked="checked" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_users" '
                                  'data-user-id="2" '
                                  'title="Can manage your users" '
                                  '/>'))

            output = check_perm_template(superman, fred,
                                         'kanisa.manage_social')

            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_social" '
                                  'data-user-id="2" '
                                  'title="Can manage your social networks" '
                                  '/>'))

        # Bob doesn't have access to either
        with self.assertNumQueries(2):
            output = check_perm_template(superman, bob,
                                         'kanisa.manage_users')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_users" '
                                  'data-user-id="1" '
                                  'title="Can manage your users" '
                                  '/>'))

            output = check_perm_template(superman, bob,
                                         'kanisa.manage_social')
            self.assertHTMLEqual(output,
                                 ('<input '
                                  'type="checkbox" '
                                  'class="kanisa_user_perm" '
                                  'data-permission-id="kanisa.manage_social" '
                                  'data-user-id="1" '
                                  'title="Can manage your social networks" '
                                  '/>'))
