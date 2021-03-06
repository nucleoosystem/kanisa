from datetime import date, timedelta
from django.utils import formats
from kanisa.models import diary
from kanisa.models import RegularEvent, ScheduledEvent


def datetime_to_string(dt):
    formatted_date = formats.date_format(dt,
                                         "DATE_FORMAT")
    formatted_time = formats.date_format(dt,
                                         "TIME_FORMAT")
    return '%s at %s' % (formatted_date, formatted_time)


def get_week_bounds(containing=None):
    if not containing:
        containing = date.today()

    monday = containing - timedelta(days=containing.weekday())
    sunday = monday + timedelta(days=6)
    return (monday, sunday)


def event_covers_date(event, thedate):
    if event.end_date is not None:
        # If the event starts after our target date, or ends before
        # it, the event does not cover our target date. Otherwise, it
        # does.
        if event.date > thedate:
            return False
        if event.end_date < thedate:
            return False

        return True

    return event.date == thedate


def get_this_week(containing=None):
    monday, sunday = get_week_bounds(containing)
    events = ScheduledEvent.events_between(monday, sunday)

    thisweek = []

    for i in range(0, 7):
        thedate = monday + timedelta(days=i)
        thisweek.append((thedate,
                        [e for e in events
                         if event_covers_date(e, thedate)]))

    return {
        'previous_week': monday - timedelta(days=1),
        'events': thisweek,
        'next_week': sunday + timedelta(days=1)
    }


class DaySchedule(object):
    def __init__(self, day, thedate, regular_events, scheduled_events):
        self.date = thedate
        self.day = day
        self.dayname = diary.DAYS_OF_WEEK[day][1]
        self.scheduled_events = []

        for event in scheduled_events:
            if not event_covers_date(event, self.date):
                continue

            self.scheduled_events.append(event)

        self.regular_events = []

        tomorrow = self.date + timedelta(days=1)

        for event in regular_events:
            dates = event.get_matching_dates(self.date, tomorrow)

            if len(dates) == 0:
                continue

            scheduled = False

            for scheduled_event in self.scheduled_events:
                if event == scheduled_event.event:
                    scheduled = True
                    break

            if scheduled:
                continue

            self.regular_events.append(event)


class WeekSchedule(object):
    def __init__(self, thedate=None):
        self.date = thedate

        if not self.date:
            self.date = date.today()

        self.monday, self.sunday = get_week_bounds(self.date)

        regular_events = RegularEvent.objects.all().order_by('start_time')

        scheduled = ScheduledEvent.events_between(self.monday,
                                                  self.sunday)

        self.calendar_entries = []

        self.events_to_schedule = False

        for i in range(0, 7):
            this_date = self.monday + timedelta(days=i)
            day_schedule = DaySchedule(i,
                                       this_date,
                                       regular_events,
                                       scheduled)
            self.calendar_entries.append(day_schedule)

            if [s for s in day_schedule.regular_events if s.autoschedule]:
                self.events_to_schedule = True


def get_schedule(thedate=None):
    return WeekSchedule(thedate)
