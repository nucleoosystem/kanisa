from django.core.urlresolvers import reverse
from kanisa.models import ScheduledEvent
from kanisa.tests.utils import KanisaViewTestCase


class DiaryManagementViewTest(KanisaViewTestCase):
    fixtures = ['diary.json', ]

    def test_views_protected(self):
        self.check_staff_only(reverse('kanisa_manage_diary'))
        self.check_staff_only(reverse('kanisa_manage_diary_regularevents'))

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

    def test_diary_regular_events_view(self):
        url = reverse('kanisa_manage_diary_regularevents')
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp,
                                'kanisa/management/diary/regular_events.html')
        self.assertTrue('regularevent_list' in resp.context)
        self.assertEqual(len(resp.context['regularevent_list']), 2)

    def test_diary_schedule_regular_event(self):
        # Check preconditions
        self.assertEqual(len(ScheduledEvent.objects.all()), 0)

        url = reverse('kanisa_manage_diary_schedule_regular_event',
                      args=[1, 20120103, ])
        self.client.login(username='fred', password='secret')

        # Schedule the event
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         ['Afternoon Tea scheduled for 3 Jan 2012 at 2 p.m.',
                          ])
        self.assertEqual(len(ScheduledEvent.objects.all()), 1)

        # shouldn't be able to schedule it again
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [('Afternoon Tea already scheduled for 3 Jan 2012 at '
                           '2 p.m.'),
                          ])

    def test_diary_schedule_nonexistent_regular_event_404s(self):
        url = reverse('kanisa_manage_diary_schedule_regular_event',
                      args=[30, 20120101, ])
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_diary_schedule_regular_event_baddate_404s(self):
        url = reverse('kanisa_manage_diary_schedule_regular_event',
                      args=[1, 20121301, ])
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
