from __future__ import absolute_import

from django.db import models
from django.db.models import Count
from sorl.thumbnail import ImageField

from kanisa.models.bible.db_field import BiblePassageField
from .base import SearchableModel


class SermonSeriesManager(models.Manager):
    def get_query_set(self):
        qs = super(SermonSeriesManager, self).get_query_set()
        return qs.annotate(the_num_sermons=Count('sermon'))


class SermonSeries(SearchableModel):
    title = models.CharField(max_length=60,
                             help_text='The name of the series.')
    image = ImageField(upload_to='kanisa/sermons/series/',
                       help_text=u'Must be at least 400px by 300px.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the series '
                                          'cover?'))
    active = models.BooleanField(default=True,
                                 help_text='Is this series currently ongoing?')
    passage = BiblePassageField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    objects = SermonSeriesManager()

    def __unicode__(self):
        return self.title

    def num_sermons(self):
        return self.the_num_sermons

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-active', )
        verbose_name_plural = 'Sermon series'


class SpeakerManager(models.Manager):
    def get_query_set(self):
        qs = super(SpeakerManager, self).get_query_set()
        return qs.annotate(num_sermons=Count('sermon'))


class SermonSpeaker(models.Model):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    image = ImageField(upload_to='kanisa/sermons/speakers/',
                       help_text=u'Must be at least 400px by 300px.')
    modified = models.DateTimeField(auto_now=True)

    objects = SpeakerManager()

    def __unicode__(self):
        return '%s %s' % (self.forename, self.surname)

    def name(self):
        return unicode(self)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('surname', 'forename', )


class SermonManager(models.Manager):
    def get_query_set(self):
        qs = super(SermonManager, self).get_query_set()
        return qs.select_related(depth=1)


class Sermon(SearchableModel):
    title = models.CharField(max_length=60,
                             help_text='The title of the sermon.')
    date = models.DateField(help_text='The date the sermon was preached.')
    series = models.ForeignKey(SermonSeries,
                               blank=True, null=True,
                               help_text=('What series the sermon is from, if '
                                          'any.'))
    speaker = models.ForeignKey(SermonSpeaker)
    passage = BiblePassageField(blank=True, null=True)
    mp3 = models.FileField(blank=True,
                           null=True,
                           upload_to='kanisa/sermons/mp3s/%Y/',
                           max_length=200,
                           verbose_name='MP3')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the sermon '
                                          'cover?'))
    modified = models.DateTimeField(auto_now=True)

    objects = SermonManager()

    def __unicode__(self):
        return self.title

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-date', )
