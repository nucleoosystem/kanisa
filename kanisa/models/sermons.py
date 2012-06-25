from django.db import models
from django.db.models import Count
from sorl.thumbnail import ImageField

from kanisa.models.bible.db_field import BiblePassageField


class SermonSeriesManager(models.Manager):
    def get_query_set(self):
        qs = super(SermonSeriesManager, self).get_query_set()
        return qs.annotate(the_num_sermons=Count('sermon'))


class SermonSeries(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the series.')
    image = ImageField(upload_to='kanisa/sermons/',
                       help_text=u'Must be at least 400px by 300px.')
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the series '
                                          'cover?'))
    active = models.BooleanField(default=True,
                                 help_text='Is this series currently ongoing?')
    passage = BiblePassageField(blank=True, null=True)

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


class SermonSpeaker(models.Model):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s %s' % (self.forename, self.surname)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('surname', 'forename', )


class Sermon(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The title of the sermon.')
    date = models.DateField(help_text='The date the sermon was preached.')
    series = models.ForeignKey(SermonSeries,
                               blank=True, null=True,
                               help_text=('What series the sermon is from, if '
                                          'any.'))
    speaker = models.ForeignKey(SermonSpeaker)
    passage = BiblePassageField(blank=True, null=True)
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the sermon '
                                          'cover?'))

    def __unicode__(self):
        return self.title

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-date', )
