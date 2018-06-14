from django.db import models
from kanisa.fields import KanisaAutoSlugField
from sorl.thumbnail import ImageField


class InlineImage(models.Model):
    title = models.CharField(max_length=60,
                             help_text=('This will be used to help you find '
                                        'it later.'))
    slug = KanisaAutoSlugField(populate_from='title')
    image = ImageField(
        upload_to='kanisa/media/',
        help_text=(
            'Image will be: '
            '<ul>'
            '<li>960x200px for headline images (the image will be cropped to '
            'fit);</li>'
            '<li>260x260px for medium images (resized without cropping);</li>'
            '<li>174x174px for small images (resized without cropping).</li>'
            '</ul>'
        )
    )
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
