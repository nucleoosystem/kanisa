from django.core.urlresolvers import reverse
from kanisa.tests.utils import KanisaViewTestCase


class DiaryManagementViewTestCase(KanisaViewTestCase):
    fixtures = ['diary.json', ]

    def test_views_protected(self):
        self.check_staff_only(reverse('kanisa_manage_diary'))

    def test_diary_root_view(self):
        url = reverse('kanisa_manage_diary')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'kanisa/management/diary/index.html')
        self.assertTrue('calendar' in resp.context)
        self.assertTrue('events_to_schedule' in resp.context)
        self.assertTrue(resp.context['events_to_schedule'])
        self.assertEqual(len(resp.context['calendar']), 7)
