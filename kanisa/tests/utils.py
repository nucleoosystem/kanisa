from django.contrib.auth.models import User, Permission
from django.test import TestCase


class KanisaViewTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create_user('bob', '', 'secret')
        bob.is_staff = False
        bob.save()

        fred = User.objects.create_user('fred', '', 'secret')
        fred.is_staff = True
        p = Permission.objects.get(codename='manage_banners')
        fred.user_permissions.add(p)
        fred.save()

    def view_is_restricted(self, url):
        # Not logged in
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        expected = 'http://testserver/accounts/login/?next=%s' % url
        self.assertEqual(resp.items()[-1],
                         ('Location', expected))

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        self.client.logout()
