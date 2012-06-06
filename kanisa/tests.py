from django.core.files.storage import default_storage
from django.test import TestCase
from kanisa.models import Banner
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
