from datetime import date
from django.contrib.auth.models import User
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


class FutureServicesManager(models.Manager):
    def get_query_set(self):
        qs = super(FutureServicesManager, self).get_query_set()
        qs = qs.filter(event__date__gte=date.today())
        return qs


class Service(models.Model):
    event = models.ForeignKey(ScheduledEvent, unique=True)
    band_leader = models.ForeignKey(User)
    songs = models.ManyToManyField(Song, through='SongInService')

    objects = models.Manager()
    future_objects = FutureServicesManager()

    def __unicode__(self):
        return unicode(self.event)

    class Meta:
        app_label = 'kanisa'
        verbose_name = 'Service Plan'


class SongInService(models.Model):
    song = models.ForeignKey(Song)
    service = models.ForeignKey(Service)
    order = models.IntegerField(default=1)

    def __unicode__(self):
        return '%s (%s)' % (self.song, self.service)

    class Meta:
        app_label = 'kanisa'
        verbose_name = 'Song'
        ordering = ('order', )
