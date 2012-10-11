from django.db import models


KNOWN_BLOCKS = {
    'homepage': ('Homepage Welcome',
                 'Appears on the homepage at the top.'),
    'address': ('Address',
                'Appears on the homepage under the contact us section.'),
    }


class Block(models.Model):
    slug = models.SlugField(unique=True)
    contents = models.TextField(blank=True,
                                null=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return KNOWN_BLOCKS[self.slug][0]

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-modified', )
        permissions = (
            ('manage_blocks',
             'Can manage your content blocks.'),
            )
