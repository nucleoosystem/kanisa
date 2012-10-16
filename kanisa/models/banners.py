from datetime import date, timedelta
from django.db import models
from django.db.models import Q
from sorl.thumbnail import ImageField

from kanisa.utils.banners import date_has_passed, today_in_range


class ActiveBannerManager(models.Manager):
    def get_query_set(self):
        qs = super(ActiveBannerManager, self).get_query_set()
        qs = qs.exclude(publish_from__gt=date.today())
        qs = qs.exclude(publish_until__lt=date.today())
        return qs


class InactiveBannerManager(models.Manager):
    def get_query_set(self):
        qs = super(InactiveBannerManager, self).get_query_set()
        not_yet_active = Q(publish_from__gt=date.today())
        expired = Q(publish_until__lt=date.today())
        return qs.filter(not_yet_active | expired)


class Banner(models.Model):
    headline = models.CharField(max_length=60,
                                help_text=('Keep this short, summarise your '
                                           'banner in a few words.'))
    contents = models.TextField(blank=True,
                                null=True,
                                help_text=('At most two sentences, give extra '
                                           'details about what you\'re '
                                           'advertising.'))
    image = ImageField(upload_to='kanisa/banners/',
                       help_text='Must be at least 800px by 600px.')
    link_text = models.CharField(max_length=60,
                                 blank=True,
                                 null=True,
                                 help_text=('The text that users will click '
                                            ' on to visit the URL for this '
                                            'banner.'))
    url = models.URLField(verbose_name='URL',
                          blank=True,
                          null=True,
                          help_text=('The web address your banner will link '
                                     'to.'))
    publish_from = models.DateField(blank=True,
                                    null=True,
                                    help_text=('The date at which your banner '
                                               'will become visible on the '
                                               'website. If left blank the '
                                               'start date is unrestricted.'))
    publish_until = models.DateField(blank=True,
                                     null=True,
                                     help_text=('The final date on which your '
                                                'banner will be visible. If '
                                                'left blank your banner will '
                                                'be visible indefinitely.'))
    visits = models.IntegerField(default=0,
                                 help_text=('The number of click-throughs '
                                            'this banner has had.'))
    modified = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()
    active_objects = ActiveBannerManager()
    inactive_objects = InactiveBannerManager()

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_banners',
             'Can manage your banners'),
        )
        ordering = ('publish_from', '-publish_until')

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
