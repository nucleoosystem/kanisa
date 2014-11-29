from django.core.cache import cache
from django.db import models


KNOWN_BLOCKS = {
    'homepage': (
        'Homepage Welcome',
        'Appears on the homepage at the top.'
    ),
    'address': (
        'Address',
        'Appears on the homepage under the contact us section.'
    ),
    'members_welcome': (
        'Members\' Welcome',
        'Appears after login by non-staff members.'
    ),
    'footer': (
        'Footer Contact',
        (
            'Appears in the right-hand side of the footer on every public '
            'page.'
        )
    ),
    'blog_intro': (
        'Blog Introduction',
        'Appears in the sidebar on event page of the blog.'
    ),
    'seasonal': (
        'Seasonal Footer',
        'Appears at the bottom of seasonal (Christmas/Easter) pages.'
    ),
    'seasonal_intro_christmas': (
        'Christmas Intro',
        'Appears at the bottom of the seasonal Christmas page.'
    ),
    'seasonal_intro_easter': (
        'Easter Intro',
        'Appears at the bottom of the seasonal Easter page.'
    ),
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
             'Can manage your content blocks'),
        )
