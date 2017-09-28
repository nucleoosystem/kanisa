from datetime import date
from django.conf import settings
from django.db import models
from kanisa.models import ScheduledEvent


class Composer(models.Model):
    forename = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.full_name()

    def full_name(self):
        return '%s %s' % (self.forename, self.surname)

    def full_name_reversed(self):
        return '%s, %s' % (self.surname, self.forename)
    full_name_reversed.admin_order_field = 'surname'
    full_name_reversed.short_description = 'Name'

    class Meta:
        app_label = 'kanisa'
        ordering = ('surname', 'forename', )


class Song(models.Model):
    title = models.CharField(max_length=100)
    composers = models.ManyToManyField(Composer, blank=True)

    def __unicode__(self):
        return self.title

    def composer_list(self):
        return list(self.composers.all())

    class Meta:
        app_label = 'kanisa'
        ordering = ('title', )


class ServicesManager(models.Manager):
    def get_queryset(self):
        qs = super(ServicesManager, self).get_queryset()
        qs = qs.select_related('band_leader', 'event', 'event__event')
        return qs


class FutureServicesManager(ServicesManager):
    def get_queryset(self):
        qs = super(FutureServicesManager, self).get_queryset()
        qs = qs.filter(event__date__gte=date.today())
        return qs


class Service(models.Model):
    event = models.OneToOneField(ScheduledEvent)
    band_leader = models.ForeignKey(settings.AUTH_USER_MODEL)
    songs = models.ManyToManyField(Song, through='SongInService')
    musicians = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='service_musicians',
        blank=True,
    )

    objects = ServicesManager()
    future_objects = FutureServicesManager()

    def __unicode__(self):
        return unicode(self.event)

    def event_title(self):
        return self.event.title

    def event_date(self):
        return self.event.date

    class Meta:
        app_label = 'kanisa'
        ordering = ('event__date', )
        permissions = (
            ('manage_services',
             'Can manage service plans'),
        )
        verbose_name = 'Service Plan'


class SongInService(models.Model):
    song = models.ForeignKey(Song)
    service = models.ForeignKey(Service)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s (%s)' % (self.song, self.service)

    class Meta:
        app_label = 'kanisa'
        ordering = ('order', )
        verbose_name = 'Song'


class BandManager(models.Manager):
    def get_queryset(self):
        qs = super(BandManager, self).get_queryset()
        qs = qs.select_related('band_leader')
        return qs


class Band(models.Model):
    band_leader = models.ForeignKey(settings.AUTH_USER_MODEL)
    musicians = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='band_musicians',
    )

    objects = BandManager()

    def __unicode__(self):
        band_leader_name = self.band_leader.get_display_name()
        if band_leader_name.endswith('s'):
            return '%s\' band' % band_leader_name

        return '%s\'s band' % band_leader_name

    class Meta:
        app_label = 'kanisa'
