from datetime import date
from django.db import models
from sorl.thumbnail import ImageField


class ActiveBannerManager(models.Manager):
    def get_query_set(self):
        qs = super(ActiveBannerManager, self).get_query_set()
        qs = qs.exclude(publish_from__gt=date.today())
        qs = qs.exclude(publish_until__lt=date.today())
        return qs


class Banner(models.Model):
    headline = models.CharField(max_length=60,
                                blank=True,
                                null=True)
    contents = models.TextField(blank=True,
                                null=True)
    image = ImageField(upload_to='kanisa/banners/')
    url = models.URLField(verbose_name=u'URL',
                          blank=True,
                          null=True)
    publish_from = models.DateField(blank=True,
                                     null=True)
    publish_until = models.DateField(blank=True,
                                     null=True)

    # Managers
    objects = models.Manager()
    active_objects = ActiveBannerManager()

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'

    def __unicode__(self):
        return self.headline

    def expired(self):
        if not self.publish_until:
            return False

        today = date.today()
        return self.publish_until < today
    expired.boolean = True

    def active(self):
        if not self.publish_from and not self.publish_until:
            # This banner has no start or expiry date, and so is
            # always active.
            return True

        today = date.today()

        if self.publish_from and self.publish_from > today:
            # We've got a start date, and it's not happened yet
            return False

        if self.publish_until and self.publish_until < today:
            # We've got a finish date which has passed
            return False

        return True
    active.boolean = True
