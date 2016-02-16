from datetime import date
from django.db import models


class ActiveSiteWideNoticeManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveSiteWideNoticeManager, self).get_queryset()
        qs = qs.exclude(published=False)
        qs = qs.exclude(publish_until__lt=date.today())
        return qs


class SiteWideNotice(models.Model):
    headline = models.CharField(
        max_length=60,
        help_text=(
            'Keep this short, summarise your announcement in a few words.')
    )
    contents = models.TextField(
        help_text=(
            'This should be a few sentences at most.'
        )
    )
    created = models.DateField(
        auto_now_add=True
    )
    publish_until = models.DateField(
        help_text=(
            'The last date on which your notice will be visible.')
    )
    published = models.BooleanField(
        default=True
    )

    # Managers
    objects = models.Manager()
    active_objects = ActiveSiteWideNoticeManager()

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_sitewidenotices',
             'Can manage your banners'),
        )
        ordering = ('-publish_until', )

    def __unicode__(self):
        return self.headline

    def expired(self):
        return self.publish_until < date.today()
    expired.boolean = True
