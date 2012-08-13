from datetime import date
from django.template.loader import render_to_string
from django.test import TestCase
from kanisa.models import SermonSeries, Sermon, SermonSpeaker
import factory


class SermonSpeakerFactory(factory.Factory):
    FACTORY_FOR = SermonSpeaker
    forename = factory.Sequence(lambda n: 'John #%s' % n)
    surname = factory.Sequence(lambda n: 'Doe #%s' % n)


class SermonSeriesFactory(factory.Factory):
    FACTORY_FOR = SermonSeries
    title = factory.Sequence(lambda n: 'Series #%s' % n)


class SermonFactory(factory.Factory):
    FACTORY_FOR = Sermon
    speaker = factory.SubFactory(SermonSpeakerFactory)
    series = factory.SubFactory(SermonSeriesFactory)
    title = factory.Sequence(lambda n: 'Sermon #%s' % n)
    date = date(2012, 1, 1)


class SermonTest(TestCase):
    def testUnicode(self):
        series = SermonSeriesFactory.build(title='Series Title')
        self.assertEqual(unicode(series), 'Series Title')

        sermon = SermonFactory.build(title='Sermon Title')
        self.assertEqual(unicode(sermon), 'Sermon Title')

    def testNumSermons(self):
        series1 = SermonSeriesFactory.create()
        series2 = SermonSeriesFactory.create()

        SermonFactory.create(series=series1)
        SermonFactory.create(series=series1)
        SermonFactory.create(series=series1)

        series1 = SermonSeries.objects.get(pk=series1.pk)
        series2 = SermonSeries.objects.get(pk=series2.pk)

        with self.assertNumQueries(0):
            self.assertEqual(series1.num_sermons(), 3)
            self.assertEqual(series2.num_sermons(), 0)

        series = list(SermonSeries.objects.all())
        with self.assertNumQueries(0):
            self.assertEqual([s.num_sermons() for s in series],
                             [3, 0])

    def testGetSermonSpeakerIsFree(self):
        speaker = SermonSpeakerFactory(forename='Bugs',
                                       surname='Bunny')
        sermon = SermonFactory.create(speaker=speaker)
        sermon = Sermon.objects.get(pk=sermon.pk)

        with self.assertNumQueries(0):
            self.assertEqual(unicode(sermon.speaker), 'Bugs Bunny')

    def testGetSermonSpeakerName(self):
        speaker = SermonSpeakerFactory.build(forename='Bugs',
                                             surname='Bunny')
        self.assertEqual(speaker.name(), 'Bugs Bunny')

    def testAutoSlugForSermonSpeaker(self):
        speaker = SermonSpeaker.objects.create(forename="Mickey",
                                               surname="Mouse")
        speaker.save()
        self.assertEqual(speaker.slug, 'mickey-mouse')

    def testFetchSermonsForSeries(self):
        series1 = SermonSeriesFactory.create()
        SermonFactory.create(series=series1,
                             date=date(2012, 4, 29))
        SermonFactory.create(series=series1,
                             date=date(2012, 5, 13))
        SermonFactory.create(series=series1,
                             date=date(2012, 5, 6))

        series1 = SermonSeries.objects.get(pk=1)
        with self.assertNumQueries(1):
            sermons = list(series1.sermons())

        self.assertEqual(len(sermons), 3)

        # Sermons should be returned in date order, oldest first.
        self.assertEqual([s.date for s in sermons],
                         [date(2012, 4, 29),
                          date(2012, 5, 6),
                          date(2012, 5, 13)])

    def test_date_range(self):
        series1 = SermonSeriesFactory.create(passage='Psalms')
        SermonFactory.create(series=series1,
                             date=date(2012, 4, 29))
        SermonFactory.create(series=series1,
                             date=date(2012, 5, 13))

        # Active series have None as the end-point of the date range.
        with self.assertNumQueries(1):
            self.assertEqual(series1.date_range(),
                             (date(2012, 4, 29),
                              None))

        series1.active = False

        with self.assertNumQueries(1):
            self.assertEqual(series1.date_range(),
                             (date(2012, 4, 29),
                              date(2012, 5, 13)))

        # Series 2 has no sermons
        series2 = SermonSeriesFactory.create(passage='John 21')
        self.assertEqual(series2.sermons().count(), 0)

        with self.assertNumQueries(1):
            self.assertEqual(series2.date_range(),
                             None)

    def test_subtitle_template(self):
        def render(series):
            tmpl = 'kanisa/public/sermons/_subtitle.html'
            return render_to_string(tmpl,
                                    {'object': series}).strip()

        series1 = SermonSeriesFactory.create(passage='Psalms')
        SermonFactory.create(series=series1,
                             date=date(2012, 4, 29))
        SermonFactory.create(series=series1,
                             date=date(2012, 5, 13))

        self.assertEqual(render(series1),
                         ('<span class="subtitle">\n(A series on '
                          '<em>Psalms</em>: 29th April 2012 &ndash; '
                          ')\n</span>'))

        series1.active = False
        self.assertEqual(render(series1),
                         ('<span class="subtitle">\n(A series on '
                          '<em>Psalms</em>: 29th April 2012 &ndash; '
                          '13th May 2012)\n</span>'))

        series1.passage = None
        self.assertEqual(render(series1),
                         ('<span class="subtitle">\n(29th April 2012 '
                          '&ndash; 13th May 2012)\n</span>'))

        series1.active = True
        self.assertEqual(render(series1),
                         ('<span class="subtitle">\n(29th April 2012 '
                          '&ndash; )\n</span>'))

        # Series 2 has no sermons
        series2 = SermonSeriesFactory.create(passage='John 21')
        self.assertEqual(render(series2),
                         ('<span class="subtitle">\n(A series on '
                          '<em>John 21</em>)\n</span>'))
