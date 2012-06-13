from datetime import date, timedelta


from kanisa.models import diary
from kanisa.models import RegularEvent, DiaryEventOccurrence


def get_week_bounds(containing=None):
    if not containing:
        containing = date.today()

    monday = containing - timedelta(days=containing.weekday())
    sunday = monday + timedelta(days=6)
    return (monday, sunday)

class WeekSchedule(object):
    def __init__(self, thedate=None):
        self.date = thedate

        if not self.date:
            self.date = date.today()

        self.monday, self.sunday = get_week_bounds(self.date)

        self.regular_events = RegularEvent.objects.all()
        self.scheduled_events = DiaryEventOccurrence.objects.\
                                    exclude(date__lt=self.monday,
                                            date__gt=self.sunday)

        self.calendar_entries = []

        for i in range(0, 7):
            self.calendar_entries.append((diary.DAYS_OF_WEEK[i][1], []))

        for event in self.regular_events:
            self.calendar_entries[event.day][1].append(event)


def get_schedule():
    return WeekSchedule()
