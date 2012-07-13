from datetime import date
from django.core.urlresolvers import reverse
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.tests.utils import KanisaViewTestCase


class DiaryManagementViewTest(KanisaViewTestCase):
    fixtures = ['diary.json', ]

    def test_views_protected(self):
        prefix = 'kanisa_manage_diary'
        self.check_staff_only_302(reverse(prefix))
        self.check_staff_only_302(reverse('%s_regularevents'
                                  % prefix))
        self.check_staff_only_302(reverse('%s_schedule_weeks_regular_event'
                                          % prefix))

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

    def test_diary_root_view_bad_date(self):
        url = reverse('kanisa_manage_diary') + '?date=abc'
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
        self.assertEqual(len(resp.context['regularevent_list']), 4)

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
        expected_location = reverse('kanisa_manage_diary')
        self.assertEqual(resp.redirect_chain,
                         [('http://testserver%s?date=20120103'
                           % expected_location, 302), ])

        self.assertEqual(len(ScheduledEvent.objects.all()), 1)

        # shouldn't be able to schedule it again
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [('Afternoon Tea already scheduled for 3 Jan 2012 at '
                           '2 p.m.'),
                          ])

        expected_location = reverse('kanisa_manage_diary')
        self.assertEqual(resp.redirect_chain,
                         [('http://testserver%s?date=20120103'
                           % expected_location, 302), ])

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

    def test_diary_cancel_scheduled_event(self):
        # Check preconditions
        self.assertEqual(len(ScheduledEvent.objects.all()), 0)

        # Schedule an event
        event = RegularEvent.objects.get(pk=1)
        event.schedule(date(2012, 01, 03), date(2012, 01, 04))
        self.assertEqual(len(ScheduledEvent.objects.all()), 1)

        pk = ScheduledEvent.objects.all()[0].pk

        url = reverse('kanisa_manage_diary_cancel_scheduled_event',
                      args=[pk, ])
        self.client.login(username='fred', password='secret')
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         ['Afternoon Tea cancelled on 3 Jan 2012 at 2 p.m.',
                          ])

        expected_location = reverse('kanisa_manage_diary')
        self.assertEqual(resp.redirect_chain,
                         [('http://testserver%s?date=20120103'
                           % expected_location, 302), ])
        self.assertEqual(len(ScheduledEvent.objects.all()), 0)

    def test_diary_cancel_scheduled_event_nonexistent_404s(self):
        # Check preconditions
        self.assertEqual(len(ScheduledEvent.objects.all()), 0)

        url = reverse('kanisa_manage_diary_cancel_scheduled_event',
                      args=[40, ])

        self.client.login(username='fred', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_diary_schedule_weeks_events(self):
        # Check preconditions
        self.assertEqual(len(ScheduledEvent.objects.all()), 0)
        url = reverse('kanisa_manage_diary_schedule_weeks_regular_event')

        # Scheduling events should schedule them
        self.client.login(username='fred', password='secret')
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [('I\'ve scheduled this week\'s events for you - '
                           'enjoy!'), ])

        self.assertEqual(len(ScheduledEvent.objects.all()), 3)

        # Trying again should error out
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('messages' in resp.context)
        self.assertEqual([m.message for m in resp.context['messages']],
                         [('No events to schedule.'), ])
        self.assertEqual(len(ScheduledEvent.objects.all()), 3)
