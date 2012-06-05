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

    def testBasics(self):
        banners = Banner.objects.all()
        self.assertEqual(len(banners), 3)
