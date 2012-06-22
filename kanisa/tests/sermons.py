from django.core.files.storage import default_storage
from django.test import TestCase
from kanisa.models import SermonSeries
import os


class SermonTest(TestCase):
    fixtures = ['sermons.json', ]

    def setUp(self):
        media_dir = os.path.join(os.path.dirname(__file__), 'fixtures/media')
        self._old_default_storage_location = default_storage.location
        default_storage.location = media_dir

    def tearDown(self):
        default_storage.location = self._old_default_storage_location

    def testUnicode(self):
        series = SermonSeries.objects.all()
        self.assertEqual(len(series), 3)
        self.assertEqual(unicode(series[0]), 'The Psalms')
        self.assertEqual(unicode(series[1]), 'All Sorts of Things')
        self.assertEqual(unicode(series[2]), 'The Beatitudes')

    def testNumSermons(self):
        series1 = SermonSeries.objects.get(pk=1)
        series2 = SermonSeries.objects.get(pk=2)
        series3 = SermonSeries.objects.get(pk=3)

        with self.assertNumQueries(0):
            self.assertEqual(series1.num_sermons(), 3)

        with self.assertNumQueries(0):
            self.assertEqual(series2.num_sermons(), 0)

        with self.assertNumQueries(0):
            self.assertEqual(series2.num_sermons(), 0)
