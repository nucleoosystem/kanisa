from datetime import date, timedelta
from django.db import models
from kanisa.models.utils import date_has_passed, today_in_range
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
        """Returns whether or not this banner has expired.

        A banner has expired if it has an expiration date, and that expiration
        date has passed.

        """

        return date_has_passed(self.publish_until)
    expired.boolean = True

    def active(self):
        """Returns whether or not this banner is currently active.

        A banner is active if either it has no publication date, or the
        publication date is in the past, and either it has no expiration date,
        or the expiration date is in the future.

        Banners are considered active if their publication date or expiration
        date are the current day.

        """

        return today_in_range(self.publish_from, self.publish_until)
    active.boolean = True

    def set_retired(self):
        """Sets the expiration date of this banner to yesterday,
        thereby removing it from the list of active banners.

        """
        self.publish_until = date.today() - timedelta(days=1)
        self.save()
