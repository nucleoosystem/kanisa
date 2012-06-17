from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class ManagementViewTest(KanisaViewTestCase):

    def test_views_protected(self):
        self.check_staff_only(reverse('kanisa.views.manage'))

    def test_root_view(self):
        url = reverse('kanisa.views.manage')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')
