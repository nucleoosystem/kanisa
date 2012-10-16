from __future__ import absolute_import

from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
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
    slug = AutoSlugField(populate_from='title', unique=True)
    image = ImageField(upload_to='kanisa/sermons/series/',
                       help_text=('This will be used in most places where the '
                                  'series is shown on the site. Must be at '
                                  'least 400px by 300px.'))
    intro = models.TextField(blank=True, null=True,
                             help_text=('Sum up this series in a few '
                                        'sentences. In some places this may '
                                        'be displayed without the details '
                                        'section below.'))
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the series '
                                          'cover?'))
    active = models.BooleanField(default=True,
                                 help_text='Is this series currently ongoing?')
    passage = BiblePassageField(blank=True, null=True,
                                help_text=('NB. This doesn\'t currently '
                                           'support multiple passages.'))
    modified = models.DateTimeField(auto_now=True)

    objects = SermonSeriesManager()

    def __unicode__(self):
        return self.title

    def num_sermons(self):
        return self.the_num_sermons

    def sermons(self):
        return self.sermon_set.order_by('date').all()

    def date_range(self):
        """Returns a (first_date, last_date) tuple representing the
        date of the first sermon and the date of the last sermon. If
        the series is currently active (implying the last sermon has
        not yet been added to the series), the second element in the
        tuple will be None. If the series has no sermons, None will be
        returned.

        """
        sermons = list(self.sermons().only('date'))

        if not sermons:
            return None

        first_sermon = sermons[0]
        if self.active:
            return (first_sermon.date, None)

        last_sermon = sermons[-1]
        return (first_sermon.date, last_sermon.date)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-active', )
        verbose_name_plural = 'Sermon series'
        permissions = (
            ('manage_sermons',
             'Can manage your sermons'),
        )


class SpeakerManager(models.Manager):
    def get_query_set(self):
        qs = super(SpeakerManager, self).get_query_set()
        return qs.annotate(num_sermons=Count('sermon'))


def sermon_speaker_slug(speaker):
    return '%s %s' % (speaker.forename, speaker.surname)


class SermonSpeaker(models.Model):
    forename = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=sermon_speaker_slug, unique=True)
    image = ImageField(upload_to='kanisa/sermons/speakers/',
                       help_text='Must be at least 400px by 300px.')
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
        verbose_name = 'Speaker'


class SermonManager(models.Manager):
    def get_query_set(self):
        qs = super(SermonManager, self).get_query_set()
        return qs.select_related(depth=1)


class Sermon(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The title of the sermon.')
    slug = AutoSlugField(populate_from='title', unique=True)
    date = models.DateField(help_text='The date the sermon was preached.')
    series = models.ForeignKey(SermonSeries,
                               blank=True, null=True,
                               help_text=('What series the sermon is from, if '
                                          'any - you can add a series using '
                                          '<a href="/manage/sermons/series/'
                                          'create/">this form</a>.'))
    speaker = models.ForeignKey(SermonSpeaker,
                                help_text=('You can add a speaker using '
                                           '<a href="/manage/sermons/speaker/'
                                           'create/">this form</a>.'))
    passage = BiblePassageField(blank=True, null=True,
                                help_text=('NB. This doesn\'t currently '
                                           'support multiple passages.'))
    mp3 = models.FileField(blank=True,
                           null=True,
                           upload_to='kanisa/sermons/mp3s/%Y/',
                           max_length=200,
                           verbose_name='MP3',
                           help_text=('The MP3 will automatically have ID3 '
                                      'data filled in (e.g. title, genre).'))
    details = models.TextField(blank=True, null=True,
                               help_text=('e.g. What themes does the sermon '
                                          'cover?'))
    modified = models.DateTimeField(auto_now=True)

    objects = SermonManager()

    def __unicode__(self):
        return self.title

    def url(self):
        # I'm not sure this belongs here, but I don't really like
        # having to switch on whether or not a sermon is part of a
        # series when I need the URL for a sermon. I'll revisit this
        # later.
        if not self.series:
            return reverse('kanisa_public_standalone_sermon_detail',
                           args=[self.slug, ])

        return reverse('kanisa_public_sermon_detail',
                       args=[self.series.slug, self.slug, ])

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-date', )
