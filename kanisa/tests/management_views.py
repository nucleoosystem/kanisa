from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase


class ManagementViewTests(TestCase):
    def setUp(self):
        bob = User.objects.create_user('bob', '', 'secret')
        bob.is_staff = False
        bob.save()

        fred = User.objects.create_user('fred', '', 'secret')
        fred.is_staff = True
        fred.save()

    def test_management_index_protected(self):
        url = reverse('kanisa.views.manage')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')


    def test_management_index_disallows_non_staff(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='bob', password='secret')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')

        self.client.logout()

    def test_management_index_allows_staff_in(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='fred', password='secret')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')

        self.client.logout()
