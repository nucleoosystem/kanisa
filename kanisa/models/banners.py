from django.db import models
from sorl.thumbnail import ImageField


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

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'

    def __unicode__(self):
        return self.headline
