from django.db import models


class SermonSeries(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the series.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the series '
                                          'cover?'))
    active = models.BooleanField(default=True,
                                 help_text='Is this series currently ongoing?')

    def __unicode__(self):
        return self.title

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
