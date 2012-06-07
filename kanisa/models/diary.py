from django.db import models


DAYS_OF_WEEK = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)


class DiaryEvent(models.Model):
    title = models.CharField(max_length=60)
    day = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    duration = models.IntegerField(default=60,
                                   help_text=u'Duration in minutes')
    details = models.TextField(blank=True, null=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'

    def __unicode__(self):
        return self.title


class DiaryEventOccurrence(models.Model):
    event = models.ForeignKey(DiaryEvent)
    date = models.DateField()
    title = models.CharField(max_length=60, blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'

    def __unicode__(self):
        if self.title:
            return self.title

        return self.event.title
