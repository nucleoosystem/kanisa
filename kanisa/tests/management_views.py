from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class ManagementViewTest(KanisaViewTestCase):

    def test_views_protected(self):
        self.check_staff_only_302(reverse('kanisa_manage_index'))
        self.check_staff_only_302(reverse('kanisa_manage_search'))

    def test_root_view(self):
        url = reverse('kanisa_manage_index')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/index.html')
