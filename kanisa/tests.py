from datetime import date, timedelta
from django.core.files.storage import default_storage
from django.test import TestCase
from kanisa.models import Banner, DiaryEvent, DiaryEventOccurrence
from kanisa.models.utils import date_has_passed, today_in_range
import os


class BannerTest(TestCase):
    fixtures = ['banners.json', ]

    def setUp(self):
        media_dir = os.path.join(os.path.dirname(__file__), 'fixtures/media')
        self._old_default_storage_location = default_storage.location
        default_storage.location = media_dir

    def tearDown(self):
        default_storage.location = self._old_default_storage_location

    def testIsActive(self):
        # A banner with no expiry date or publication date
        banner = Banner.objects.get(pk=1)
        self.assertTrue(banner.active())

        # A banner which has expired
        banner = Banner.objects.get(pk=4)
        self.assertFalse(banner.active())

        # A banner with a long-passed publication date, and a
        # far-future expiration date
        banner = Banner.objects.get(pk=5)
        self.assertTrue(banner.active())

    def testHasExpired(self):
        # A banner with no expiry date or publication date
        banner = Banner.objects.get(pk=1)
        self.assertFalse(banner.expired())

        # A banner which has expired
        banner = Banner.objects.get(pk=4)
        self.assertTrue(banner.expired())

        # A banner with a long-passed publication date, and a
        # far-future expiration date
        banner = Banner.objects.get(pk=5)
        self.assertFalse(banner.expired())

    def testFetchActive(self):
        banners = Banner.active_objects.all()
        self.assertEqual(len(banners), 4)

    def testUnicode(self):
        banner = Banner.objects.get(pk=1)
        self.assertEqual(unicode(banner), 'Green Flowers')

    def testDateHasPassed(self):
        self.assertFalse(date_has_passed(None))
        self.assertTrue(date_has_passed(date(2012, 1, 1)))
        self.assertFalse(date_has_passed(date.today()))

    def testTodayInRange(self):
        self.assertTrue(today_in_range(None, None))
        self.assertTrue(today_in_range(date.today(), None))
        self.assertTrue(today_in_range(None, date.today()))
        self.assertTrue(today_in_range(date.today(), date.today()))
        self.assertTrue(today_in_range(date.today() - timedelta(days=1),
                                       date.today() + timedelta(days=1)))
        self.assertFalse(today_in_range(date.today() - timedelta(days=1),
                                        date.today() - timedelta(days=1)))
        self.assertFalse(today_in_range(date.today() + timedelta(days=1),
                                        date.today() + timedelta(days=1)))
        self.assertFalse(today_in_range(date.today() + timedelta(days=1),
                                        None))
        self.assertFalse(today_in_range(None,
                                        date.today() - timedelta(days=1)))


class DiaryTest(TestCase):
    fixtures = ['diary.json', ]

    def testUnicode(self):
        event = DiaryEvent.objects.get(pk=1)
        self.assertEqual(unicode(event), 'Afternoon Tea')

    def testSchedule(self):
        event = DiaryEvent.objects.get(pk=1)
        self.assertEqual(event.day, 1)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instances = event.diaryeventoccurrence_set.all()
        self.assertEqual(len(instances), 1)

        instance = instances[0]
        self.assertEqual(instance.date, date(2012, 1, 3))

    def testInstanceUnicode(self):
        event = DiaryEvent.objects.get(pk=2)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instance = DiaryEventOccurrence.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Breakfast Club')
        instance.title = 'Special Breakfast'
        instance.save()

        instance = DiaryEventOccurrence.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Special Breakfast')
