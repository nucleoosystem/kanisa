from __future__ import absolute_import

from autoslug import AutoSlugField
from datetime import datetime, timedelta
from django.db import models
from recurrence.fields import RecurrenceField
from sorl.thumbnail import ImageField

from .base import SearchableModel


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class RegularEvent(SearchableModel):
    title = models.CharField(max_length=60,
                             help_text='The name of the event.')
    image = ImageField(upload_to='kanisa/diary/events/',
                       help_text=u'Must be at least 200px by 200px.')
    slug = AutoSlugField(populate_from='title', unique=True)
    day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK,
                                           help_text=('What day of the week '
                                                      'does this event '
                                                      'happen on?'))
    pattern = RecurrenceField(blank=True, null=True, verbose_name='Timetable')
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(default=60,
                                   help_text=u'Duration in minutes.')
    intro = models.CharField(max_length=200,
                             help_text=('Brief description (no Markdown here) '
                                        'of what the event is and who it is '
                                        'for.'))
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. Who is this event for? What '
                                          'does it involve? How much does it '
                                          'cost? Where is it held?'))
    autoschedule = models.BooleanField(default=True,
                                       verbose_name='auto-schedule',
                                       help_text=('Uncheck this to not '
                                                  'auto-schedule this event '
                                                  'when bulk-scheduling.'))
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('title', )
        permissions = (
            ('manage_diary',
             'Can manage your diary'),
            )

    def __unicode__(self):
        return self.title

    def schedule(self, start_date, end_date):
        """Schedule an instance of this event, with no custom details
        set up. The instance will be scheduled for all matching dates
        on or after start_date, and before (and not including)
        end_date.
        """

        def daterange(start_date, end_date):
            for n in range((end_date - start_date).days):
                yield start_date + timedelta(n)

        for single_date in daterange(start_date, end_date):
            if single_date.weekday() != self.day:
                continue

            self.scheduledevent_set.\
                create(date=single_date,
                       title=self.title,
                       start_time=self.start_time,
                       duration=self.duration)

    class AlreadyScheduled(Exception):
        pass

    def schedule_once(self, date):
        event_exists = ScheduledEvent.objects.filter(event=self,
                                                     date=date)
        if len(event_exists) != 0:
            raise RegularEvent.AlreadyScheduled()

        self.schedule(date, date + timedelta(days=1))

    def get_next(self):
        events = ScheduledEvent.objects.filter(event=self,
                                               date__gte=datetime.now())[:1]

        if not events:
            return None

        return events[0]

    def pattern_description(self):
        if self.pattern and len(self.pattern.rrules) == 1:
            text = self.pattern.rrules[0].to_text()
            return text[0].capitalize() + text[1:]

        return 'Unknown'


class ScheduledEvent(SearchableModel):
    event = models.ForeignKey(RegularEvent, blank=True, null=True,
                              help_text=('You can leave this blank, but if '
                                         'you do you must give the event a '
                                         'title.'))
    title = models.CharField(max_length=60)
    date = models.DateField()
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(default=60,
                                   help_text=u'Duration in minutes.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. Who is this event for? What '
                                          'does it involve? How much does it '
                                          'cost? Where is it held?'))
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('date', 'start_time')

    def __unicode__(self):
        if self.title:
            return self.title

        if self.event:
            return self.event.title

        # Hopefully this only occurs during event editing
        return u'None'
