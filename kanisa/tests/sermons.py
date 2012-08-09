from datetime import date
from django.core.files.storage import default_storage
from django.test import TestCase
from kanisa.models import SermonSeries, Sermon, SermonSpeaker
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

        sermon = Sermon.objects.get(pk=1)
        self.assertEqual(unicode(sermon), 'Something about Psalm 1')

    def testNumSermons(self):
        series1 = SermonSeries.objects.get(pk=1)
        series2 = SermonSeries.objects.get(pk=2)
        series3 = SermonSeries.objects.get(pk=3)

        with self.assertNumQueries(0):
            self.assertEqual(series1.num_sermons(), 3)
            self.assertEqual(series2.num_sermons(), 0)
            self.assertEqual(series3.num_sermons(), 0)

        series = list(SermonSeries.objects.all())
        with self.assertNumQueries(0):
            self.assertEqual([s.num_sermons() for s in series],
                             [3, 0, 0])

    def testGetSermonSpeakerIsFree(self):
        sermon = Sermon.objects.get(pk=1)

        with self.assertNumQueries(0):
            self.assertEqual(unicode(sermon.speaker), 'Bugs Bunny')

    def testGetSermonSpeakerName(self):
        speaker = SermonSpeaker.objects.get(pk=1)
        self.assertEqual(speaker.name(), 'Bugs Bunny')

    def testAutoSlugForSermonSpeaker(self):
        speaker = SermonSpeaker.objects.create(forename="Mickey",
                                               surname="Mouse")
        speaker.save()
        self.assertEqual(speaker.slug, 'mickey-mouse')

    def testFetchSermonsForSeries(self):
        series1 = SermonSeries.objects.get(pk=1)
        with self.assertNumQueries(1):
            sermons = list(series1.sermons())

        self.assertEqual(len(sermons), 3)

        # Sermons should be returned in date order, oldest first.
        self.assertEqual([s.date for s in sermons],
                         [date(2012, 4, 29),
                          date(2012, 5, 6),
                          date(2012, 5, 13)])
