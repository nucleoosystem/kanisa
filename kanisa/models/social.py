from django.db import models


class FutureScheduledTweetsManager(models.Manager):
    def get_queryset(self):
        qs = super(FutureScheduledTweetsManager, self).get_queryset()
        qs = qs.exclude(posted=True)
        return qs


class ScheduledTweet(models.Model):
    tweet = models.CharField(max_length=140)
    date = models.DateField()
    time = models.TimeField()
    posted = models.BooleanField(default=False,
                                 help_text=('Whether or not this Tweet has '
                                            'been posted to Twitter.'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()
    future_objects = FutureScheduledTweetsManager()

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('date', 'time', )
        permissions = (
            ('manage_social',
             'Can manage your social networks'),
        )

    def __unicode__(self):
        return self.tweet
