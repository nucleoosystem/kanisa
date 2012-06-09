from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase


class ManagementViewTests(TestCase):
    fixtures = ['banners.json', ]

    def setUp(self):
        bob = User.objects.create_user('bob', '', 'secret')
        bob.is_staff = False
        bob.save()

        fred = User.objects.create_user('fred', '', 'secret')
        fred.is_staff = True
        fred.save()

    def test_views_protected(self):
        self.__test_staff_only('kanisa.views.manage')
        self.__test_staff_only('kanisa.views.manage_banners')

    def test_root_view(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')

    def test_banner_management_view(self):
        url = reverse('kanisa.views.manage_banners')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/banners/index.html')

        self.assertTrue('banners' in resp.context)
        self.assertEqual([banner.pk for banner in resp.context['banners']],
                         [1, 2, 3, 5, ])

    def __test_staff_only(self, view_name):
        # Not logged in
        url = reverse(view_name)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')
        self.client.logout()
