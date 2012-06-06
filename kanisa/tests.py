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
        banner = Banner.objects.get(pk=1)
        self.assertTrue(banner.active())

    def testHasExpired(self):
        banner = Banner.objects.get(pk=1)
        self.assertFalse(banner.expired())        

    def testFetchActive(self):
        banners = Banner.active_objects.all()
        self.assertEqual(len(banners), 3)

    def testUnicode(self):
        banner = Banner.objects.get(pk=1)
        self.assertEqual(unicode(banner), 'Green Flowers')
