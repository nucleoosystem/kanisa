from datetime import date, time
from django.test import TestCase
from kanisa.models import diary
from kanisa.models import RegularEvent, ScheduledEvent
from kanisa.utils.diary import get_week_bounds, get_schedule
import factory


class RegularEventFactory(factory.Factory):
    FACTORY_FOR = RegularEvent
    title = factory.Sequence(lambda n: 'Regular Event #' + n)
    start_time = time(14, 0)
    duration = 60
    day = 1


class DiaryTest(TestCase):
    def testUnicode(self):
        event = RegularEventFactory.build(title='Afternoon Tea')
        self.assertEqual(unicode(event), 'Afternoon Tea')

    def testSchedule(self):
        event = RegularEventFactory.build(day=1)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instances = event.scheduledevent_set.all()
        self.assertEqual(len(instances), 1)

        instance = instances[0]
        self.assertEqual(instance.date, date(2012, 1, 3))
        self.assertEqual(instance.start_time, time(14, 0, 0))
        self.assertEqual(instance.duration, 60)

    def testInstanceUnicode(self):
        event = RegularEventFactory.build(title='Breakfast Club',
                                          day=4)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instance = ScheduledEvent.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Breakfast Club')
        instance.title = 'Special Breakfast'
        instance.save()

        instance = ScheduledEvent.objects.get(pk=1)
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
    def testBasics(self):
        event1 = RegularEventFactory.create(day=1)
        event2 = RegularEventFactory.create(day=4)
        RegularEventFactory.create(day=2)
        RegularEventFactory.create(day=3)
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
                         [0, 1, 1, 1, 1, 0, 0])
        self.assertEqual(entries[1].regular_events[0],
                         event1)
        self.assertEqual(entries[4].regular_events[0],
                         event2)

    def testScheduled(self):
        event1 = RegularEventFactory.create(day=1)
        RegularEventFactory.create(day=2)

        event1.schedule(date(2012, 1, 1),
                        date(2012, 1, 8))
        self.assertEqual(len(ScheduledEvent.objects.all()),
                         1)
        instance = ScheduledEvent.objects.get(pk=1)
        self.assertEqual(instance.date, date(2012, 1, 3))

        schedule = get_schedule(date(2012, 1, 4))
        entries = schedule.calendar_entries

        # Regular events is a weekday aligned list of regular events
        # which are not yet scheduled.
        self.assertEqual([len(e.regular_events) for e in entries],
                         [0, 0, 1, 0, 0, 0, 0])

        # Scheduled events is a weekday aligned list of scheduled
        # events which are scheduled.
        self.assertEqual([len(e.scheduled_events) for e in entries],
                         [0, 1, 0, 0, 0, 0, 0])
