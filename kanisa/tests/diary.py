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
    pattern = ''


class DiaryTest(TestCase):
    def testUnicode(self):
        event = RegularEventFactory.build(title='Afternoon Tea')
        self.assertEqual(unicode(event), 'Afternoon Tea')

    def testSchedule(self):
        pattern = "RRULE:FREQ=WEEKLY;BYDAY=TU"
        event = RegularEventFactory.create(pattern=pattern)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instances = event.scheduledevent_set.all()
        self.assertEqual(len(instances), 1)

        instance = instances[0]
        self.assertEqual(instance.date, date(2012, 1, 3))
        self.assertEqual(instance.start_time, time(14, 0, 0))
        self.assertEqual(instance.duration, 60)

    def testInstanceUnicode(self):
        friday = "RRULE:FREQ=WEEKLY;BYDAY=FR"
        event = RegularEventFactory.create(title='Breakfast Club',
                                           pattern=friday)
        event.schedule(date(2012, 1, 1), date(2012, 1, 8))

        instance = ScheduledEvent.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Breakfast Club')
        instance.title = 'Special Breakfast'
        instance.save()

        instance = ScheduledEvent.objects.get(pk=1)
        self.assertEqual(unicode(instance), 'Special Breakfast')

    def testGetNextWithEventScheduled(self):
        tuesdays = "RRULE:FREQ=WEEKLY;BYDAY=TU"
        event = RegularEventFactory.create(title='Breakfast Club',
                                           pattern=tuesdays)

        # I should probably mock out datetime.now() here, so I don't
        # have to use such a far-future date.
        event.schedule(date(2020, 1, 1), date(2020, 1, 31))
        next = event.get_next()
        self.assertEqual(next.title, 'Breakfast Club')
        self.assertEqual(next.date, date(2020, 1, 7))

    def testGetNextWithoutEventScheduled(self):
        event = RegularEventFactory.create(title='Breakfast Club')
        next = event.get_next()
        self.assertEqual(next, None)


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
        tuesday = "RRULE:FREQ=WEEKLY;BYDAY=TU"
        wednesday = "RRULE:FREQ=WEEKLY;BYDAY=WE"
        thursday = "RRULE:FREQ=WEEKLY;BYDAY=TH"
        friday = "RRULE:FREQ=WEEKLY;BYDAY=FR"
        event1 = RegularEventFactory.create(pattern=tuesday)
        event2 = RegularEventFactory.create(pattern=friday)
        RegularEventFactory.create(pattern=wednesday)
        RegularEventFactory.create(pattern=thursday)
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
        tuesday = "RRULE:FREQ=WEEKLY;BYDAY=TU"
        event1 = RegularEventFactory.create(pattern=tuesday)
        RegularEventFactory.create(pattern="RRULE:FREQ=WEEKLY;BYDAY=WE")

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


class ScheduledEventFactory(factory.Factory):
    FACTORY_FOR = ScheduledEvent
    title = factory.Sequence(lambda n: 'Event #' + n)
    start_time = time(14, 0)
    date = date(2012, 6, 15)


class DiaryScheduledEventTest(TestCase):
    def testUnicode(self):
        event = ScheduledEventFactory.build(title='Afternoon Tea')
        self.assertEqual(unicode(event), 'Afternoon Tea')

    def testEndDate(self):
        # end_date should be auto-populated
        event1 = ScheduledEventFactory.create()
        self.assertEqual(event1.end_date, date(2012, 6, 15))

    def testEventsBetween(self):
        event1 = ScheduledEventFactory.create(title='1')
        event2 = ScheduledEventFactory.create(title='2',
                                              date=date(2012, 6, 12))
        event3 = ScheduledEventFactory.create(title='3',
                                              date=date(2012, 6, 19))
        early_event = ScheduledEventFactory.create(title='early',
                                                   date=date(2012, 6, 11))
        late_event = ScheduledEventFactory.create(title='late',
                                                  date=date(2012, 6, 20))

        events = ScheduledEvent.events_between(date(2012, 6, 12),
                                               date(2012, 6, 19))

        self.assertEqual(list(events),
                         [event2, event1, event3, ])

        events = ScheduledEvent.events_between(date(2012, 6, 11),
                                               date(2012, 6, 15))

        self.assertEqual(list(events),
                         [early_event, event2, event1, ])

        events = ScheduledEvent.events_between(date(2012, 6, 12),
                                               date(2012, 6, 20))

        self.assertEqual(list(events),
                         [event2, event1, event3, late_event, ])

    def testEventsBetweenMultiDayDuring(self):
        event1 = ScheduledEventFactory.create(end_date=date(2012, 6, 16))
        events = ScheduledEvent.events_between(date(2012, 6, 11),
                                               date(2012, 6, 15))

        self.assertEqual(list(events),
                         [event1, ])

    def testEventsBetweenMultiDayBefore(self):
        event1 = ScheduledEventFactory.create(date=date(2012, 6, 10),
                                              end_date=date(2012, 6, 16))
        # This one ends before the range we care about
        ScheduledEventFactory.create(date=date(2012, 6, 9),
                                     end_date=date(2012, 6, 10))

        events = ScheduledEvent.events_between(date(2012, 6, 11),
                                               date(2012, 6, 15))

        self.assertEqual(list(events),
                         [event1, ])

    def testEventsBetweenMultiDayAfter(self):
        event1 = ScheduledEventFactory.create(end_date=date(2012, 6, 20))

        # This one starts after the range we care about
        ScheduledEventFactory.create(date=date(2012, 6, 16),
                                     end_date=date(2012, 6, 20))

        events = ScheduledEvent.events_between(date(2012, 6, 11),
                                               date(2012, 6, 15))

        self.assertEqual(list(events),
                         [event1, ])
