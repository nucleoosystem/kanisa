from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.test.utils import override_settings


class KanisaViewTestCase(TestCase):
    def setUp(self):
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

    @override_settings(LOGIN_URL='/loginview/')
    def view_is_restricted(self, url):
        # Not logged in
        resp = self.client.get(url)

        # The loginview URL does not exist. I should probably make
        # sure it does, but for now I'll just say this should 404, and
        # set the URL to something that probably won't exist. This
        # could do with tidying up.
        self.assertRedirects(resp, '/loginview/?next=%s' % url,
                             302, 404)

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        self.client.logout()
