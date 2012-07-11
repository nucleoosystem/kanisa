from __future__ import absolute_import

from django.db import models

from .base import SearchableModel


class ScheduledTweet(SearchableModel):
    tweet = models.CharField(max_length=140)
    date = models.DateField()
    time = models.TimeField()
    posted = models.BooleanField(default=False,
                                 help_text=('Whether or not this Tweet has '
                                            'been posted to Twitter.'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('date', 'time', )

    def __unicode__(self):
        return self.tweet
