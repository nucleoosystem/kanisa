from django.core.cache import cache
from django.db import models


KNOWN_BLOCKS = {
    'homepage': ('Homepage Welcome',
                 'Appears on the homepage at the top.'),
    'address': ('Address',
                'Appears on the homepage under the contact us section.'),
    'members_welcome': ('Members\' Welcome',
                        'Appears after login by non-staff members.'),
}


class Block(models.Model):
    slug = models.SlugField(unique=True)
    contents = models.TextField(blank=True,
                                null=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return KNOWN_BLOCKS[self.slug][0]

    def save(self, *args, **kwargs):
        super(Block, self).save(*args, **kwargs)
        cache.delete('kanisa_content_block:%s' % self.slug)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-modified', )
        permissions = (
            ('manage_blocks',
             'Can manage your content blocks.'),
        )
