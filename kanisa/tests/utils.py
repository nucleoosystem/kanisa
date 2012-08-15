from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase
from django.test.utils import override_settings


class KanisaViewTestCase(TestCase):
    def setUp(self):
        self.bob = User.objects.create_user('bob', '', 'secret')
        self.bob.is_staff = False
        self.bob.save()

        self.fred = User.objects.create_user('fred', '', 'secret')
        p = Permission.objects.get(codename='manage_banners')
        self.fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_diary')
        self.fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_sermons')
        self.fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_users')
        self.fred.user_permissions.add(p)
        p = Permission.objects.get(codename='manage_pages')
        self.fred.user_permissions.add(p)

        self.fred.save()

    @override_settings(LOGIN_URL=reverse_lazy('kanisa_public_login'))
    def view_is_restricted(self, url):
        # Not logged in
        resp = self.client.get(url)
        login_url = reverse('kanisa_public_login')
        self.assertRedirects(resp, '%s?next=%s' % (login_url, url),
                             302, 200)

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)
        self.client.logout()
