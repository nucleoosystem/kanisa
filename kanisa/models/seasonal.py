from datetime import date, datetime, timedelta
from django.db import models


class SeasonalEvent(models.Model):
    SEASON_CHOICES = (
        ('E', 'Easter'),
        ('C', 'Christmas'),
    )

    season = models.CharField(
        max_length=1, choices=SEASON_CHOICES
    )
    title = models.CharField(max_length=60)
    date = models.DateField()
    start_time = models.TimeField(
        help_text='What time does the event start?'
    )
    duration = models.IntegerField(
        blank=True, null=True,
        help_text=(
            'Duration in minutes (leave '
            'blank for unknown).'
        )
    )
    intro = models.CharField(
        blank=True,
        max_length=200,
        help_text=(
            'Brief description (no Markdown here) of what the event is '
            'and who it is for.'
        )
    )

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('date', 'start_time', )

    def __unicode__(self):
        return self.title

    def end_time(self):
        dummy = datetime.combine(date(2014, 1, 1), self.start_time)
        return (dummy + timedelta(minutes=self.duration)).time()
