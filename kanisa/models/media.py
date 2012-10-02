from autoslug import AutoSlugField
from django.db import models
from sorl.thumbnail import ImageField


class InlineImage(models.Model):
    title = models.CharField(max_length=60,
                             help_text=('This will be used to help you find '
                                        'it later.'))
    slug = AutoSlugField(populate_from='title', unique=True)
    image = ImageField(upload_to='kanisa/media/')
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_media',
             'Can manage your media'),
            )

    def __unicode__(self):
        return self.title
