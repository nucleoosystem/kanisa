from datetime import date
from django.test import TestCase
from kanisa.models import diary
from kanisa.models import RegularEvent, DiaryEventOccurrence
from kanisa.utils import get_week_bounds, get_schedule


class DiaryTest(TestCase):
    fixtures = ['diary.json', ]

    def testUnicode(self):
        event = RegularEvent.objects.get(pk=1)
        self.assertEqual(unicode(event), 'Afternoon Tea')

    def testSchedule(self):
        event = RegularEvent.objects.get(pk=1)
        self.assertEqual(event.day, 1)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instances = event.diaryeventoccurrence_set.all()
        self.assertEqual(len(instances), 1)

        instance = instances[0]
        self.assertEqual(instance.date, date(2012, 1, 3))

    def testInstanceUnicode(self):
        event = RegularEvent.objects.get(pk=2)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instance = DiaryEventOccurrence.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Breakfast Club')
        instance.title = 'Special Breakfast'
        instance.save()

        instance = DiaryEventOccurrence.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Special Breakfast')


class DiaryGetWeekBoundsTest(TestCase):
    def testGetWeekBoundsToday(self):
        monday, sunday = get_week_bounds()
        self.assertEqual(monday.weekday(), 0)
        self.assertEqual(sunday.weekday(), 6)
        self.assertTrue(monday <= date.today())
        self.assertTrue(sunday >= date.today())

    def testGetWeekBoundsOnDate(self):
        monday, sunday = get_week_bounds(date(2012, 6, 12))
        self.assertEqual(monday.weekday(), 0)
        self.assertEqual(sunday.weekday(), 6)
        self.assertEqual(monday, date(2012, 6, 11))
        self.assertEqual(sunday, date(2012, 6, 17))

    def testGetWeekBoundsOnAMonday(self):
        monday, sunday = get_week_bounds(date(2012, 6, 11))
        self.assertEqual(monday.weekday(), 0)
        self.assertEqual(sunday.weekday(), 6)
        self.assertEqual(monday, date(2012, 6, 11))
        self.assertEqual(sunday, date(2012, 6, 17))

    def testGetWeekBoundsOnASunday(self):
        monday, sunday = get_week_bounds(date(2012, 6, 17))
        self.assertEqual(monday.weekday(), 0)
        self.assertEqual(sunday.weekday(), 6)
        self.assertEqual(monday, date(2012, 6, 11))
        self.assertEqual(sunday, date(2012, 6, 17))


class DiaryGetScheduleTest(TestCase):
    fixtures = ['diary.json', ]

    def testBasics(self):
        schedule = get_schedule()
        self.assertTrue(hasattr(schedule, 'calendar_entries'))
        self.assertEqual(len(schedule.calendar_entries), 7)

        entries = schedule.calendar_entries

        days_of_week = [d[1] for d in diary.DAYS_OF_WEEK]
        self.assertEqual(days_of_week,
                         [s.dayname for s in entries])
        self.assertEqual(range(0, 7),
                         [s.day for s in entries])

        self.assertEqual([len(e.regular_events) for e in entries],
                         [0, 1, 0, 0, 1, 0, 0])
        self.assertEqual(entries[1].regular_events[0],
                         RegularEvent.objects.get(pk=1))
        self.assertEqual(entries[4].regular_events[0],
                         RegularEvent.objects.get(pk=2))

    def testScheduled(self):
        event = RegularEvent.objects.get(pk=1)

        self.assertEqual(event.day, 1)
        self.assertEqual(unicode(event), 'Afternoon Tea')

        event.schedule(date(2012, 1, 1),
                       date(2012, 1, 8))
        self.assertEqual(len(DiaryEventOccurrence.objects.all()),
                         1)
        instance = DiaryEventOccurrence.objects.get(pk=1)
        self.assertEqual(instance.date, date(2012, 1, 3))

        schedule = get_schedule(date(2012, 1, 4))
        entries = schedule.calendar_entries

        self.assertEqual([len(e.regular_events) for e in entries],
                         [0, 0, 0, 0, 1, 0, 0])
        self.assertEqual([len(e.scheduled_events) for e in entries],
                         [0, 1, 0, 0, 0, 0, 0])
