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

    class Meta:
        app_label = 'kanisa'


class Service(models.Model):
    event = models.ForeignKey(ScheduledEvent)
    band_leader = models.ForeignKey(User)
    songs = models.ManyToManyField(Song, through='SongInService')

    def __unicode__(self):
        return unicode(self.event)

    class Meta:
        app_label = 'kanisa'


class SongInService(models.Model):
    song = models.ForeignKey(Song)
    service = models.ForeignKey(Service)
    order = models.IntegerField(default=1)

    class Meta:
        app_label = 'kanisa'
        verbose_name = 'Song'
