from datetime import date, datetime, timedelta, time
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Count
from kanisa.fields import KanisaAutoSlugField
from kanisa.utils.branding import BrandingInformation
from recurrence.fields import RecurrenceField
from sorl.thumbnail import ImageField


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class EventContact(models.Model):
    name = models.CharField(max_length=60,
                            help_text='The full name of the contact')
    email = models.EmailField(help_text=('Bear in mind that this will be '
                                         'displayed on a public website.'))
    image = ImageField(blank=True,
                       null=True,
                       upload_to='kanisa/diary/contacts/',
                       help_text='Must be at least 200px by 200px')

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'

    def __unicode__(self):
        return self.name

    def image_or_default(self):
        if self.image:
            return self.image

        branding = BrandingInformation('apple')
        return branding.url


class EventCategoryManager(models.Manager):
    def get_queryset(self):
        qs = super(EventCategoryManager, self).get_queryset()
        return qs.annotate(num_events=Count('regularevent'))


class EventCategory(models.Model):
    title = models.CharField(max_length=30)

    objects = EventCategoryManager()

    class Meta:
        app_label = 'kanisa'
        ordering = ('title', )
        verbose_name_plural = 'Event categories'

    def __unicode__(self):
        return self.title


class RegularEvent(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the event.')
    categories = models.ManyToManyField(EventCategory,
                                        verbose_name='Event Categories',
                                        blank=True)
    image = ImageField(upload_to='kanisa/diary/events/',
                       help_text='Must be at least 200px by 200px.')
    slug = KanisaAutoSlugField(populate_from='title')
    pattern = RecurrenceField(verbose_name='Timetable', blank=True)
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(default=60,
                                   help_text='Duration in minutes.')
    contact = models.ForeignKey(EventContact,
                                blank=True,
                                null=True)
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
    mothballed = models.BooleanField(default=False)
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

    def url(self):
        return reverse('kanisa_public_diary_regularevent_detail',
                       args=[self.slug, ])

    def get_matching_dates(self, start_date, end_date):
        """Get a list of dates which match our recurrence pattern from
        start_date and before end_date.
        """

        # We need to remove one day from the start_date, since
        # "between" is not inclusive of the start and end dates.
        tz_start_date = datetime.combine(start_date - timedelta(days=1),
                                         time())
        tz_end_date = datetime.combine(end_date, time())

        before_start_date = tz_start_date - timedelta(days=1)

        occurrences = self.pattern.between(tz_start_date, tz_end_date,
                                           dtstart=before_start_date,
                                           dtend=tz_end_date)
        return [d.date() for d in occurrences]

    def schedule(self, start_date, end_date):
        """Schedule an instance of this event, with no custom details
        set up. The instance will be scheduled for all matching dates
        on or after start_date, and before (and not including)
        end_date.
        """
        dates = self.get_matching_dates(start_date, end_date)

        for single_date in dates:
            self.scheduledevent_set.\
                create(date=single_date,
                       title=self.title,
                       intro=self.intro,
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

    def get_next(self, now=None):
        if not now:
            now = datetime.now()

        events = ScheduledEvent.objects.filter(
            event=self,
            date__gte=now,
        )
        events = events.exclude(
            date=date.today(),
            start_time__lt=now
        )
        events = events[:1]

        if not events:
            return None

        return events[0]

    def pattern_description(self):
        if not self.pattern:
            return 'None'

        if self.pattern and len(self.pattern.rrules) == 1:
            text = self.pattern.rrules[0].to_text()
            return text[0].capitalize() + text[1:]

        return 'Unknown'


class ScheduledEventSeriesManager(models.Manager):
    def get_queryset(self):
        qs = super(ScheduledEventSeriesManager, self).get_queryset()
        return qs.prefetch_related('events')


class ScheduledEventSeries(models.Model):
    name = models.CharField(max_length=100)
    objects = ScheduledEventSeriesManager()

    def __unicode__(self):
        return self.name

    def get_cached_events(self):
        if hasattr(self, 'cached_events'):
            return self.cached_events

        self.cached_events = list(self.events.all())
        return self.cached_events

    def start_date(self):
        if not self.get_cached_events():
            return None

        return self.get_cached_events()[0].date

    def end_date(self):
        if not self.get_cached_events():
            return None

        return self.get_cached_events()[-1].date

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('name', )


class ScheduledEventManager(models.Manager):
    def get_queryset(self):
        qs = super(ScheduledEventManager, self).get_queryset()
        return qs.select_related('event')


class ScheduledEvent(models.Model):
    event = models.ForeignKey(RegularEvent, blank=True, null=True,
                              help_text=('You can leave this blank, but if '
                                         'you do you must give the event a '
                                         'title.'))
    title = models.CharField(max_length=60)
    date = models.DateField()
    start_time = models.TimeField(help_text='What time does the event start?')
    duration = models.IntegerField(blank=True, null=True,
                                   help_text=('Duration in minutes (leave '
                                              'blank for unknown duration and '
                                              'for multi-day events).'))
    end_date = models.DateField(blank=True, null=True,
                                help_text=('If an end date is specified, any '
                                           'duration given will be ignored.'))
    contact = models.ForeignKey(EventContact,
                                blank=True,
                                null=True)
    intro = models.CharField(max_length=200,
                             help_text=('Brief description (no Markdown here) '
                                        'of what the event is and who it is '
                                        'for.'))
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. Who is this event for? What '
                                          'does it involve? How much does it '
                                          'cost? Where is it held?'))
    series = models.ForeignKey(
        ScheduledEventSeries,
        blank=True,
        null=True,
        related_name='events'
    )
    modified = models.DateTimeField(auto_now=True)

    objects = ScheduledEventManager()
    bare_objects = models.Manager()

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
        return 'None'

    def save(self, *args, **kwargs):
        if self.end_date is None:
            self.end_date = self.date

        super(ScheduledEvent, self).save(*args, **kwargs)

    def is_special(self):
        if not self.event:
            return True

        if self.end_date and self.end_date != self.date:
            return True

        if self.event and self.details:
            if self.event.details != self.details:
                return True

        return False

    def url(self):
        if not self.is_special():
            return reverse('kanisa_public_diary_regularevent_detail',
                           args=[self.event.slug, ])
        return reverse('kanisa_public_diary_scheduledevent_detail',
                       args=[self.pk, ])

    @classmethod
    def events_between(cls, start_date, end_date):
        events = ScheduledEvent.objects.exclude(end_date__lt=start_date)
        events = events.exclude(date__gt=end_date)
        return events
