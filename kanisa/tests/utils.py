from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase
from django.test.utils import override_settings


class KanisaViewTestCase(TestCase):
    def setUp(self):
        if hasattr(self, 'setup_called'):
            return

        bob = User.objects.create_user('bob', '', 'secret')
        bob.is_staff = False
        bob.save()

        fred = User.objects.create_user('fred', '', 'secret')
        fred.is_staff = True
        p = Permission.objects.get(codename='manage_banners')
        fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_diary')
        fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_sermons')
        fred.user_permissions.add(p)
        fred.save()

        # Only need to do all this once - we create users and then
        # never clear them up.
        self.setup_called = True

    @override_settings(LOGIN_URL=reverse_lazy('kanisa_public_login'))
    def view_is_restricted(self, url):
        # Not logged in
        resp = self.client.get(url)

        self.assertRedirects(resp, '/login/?next=%s' % url,
                             302, 200)

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        self.client.logout()
