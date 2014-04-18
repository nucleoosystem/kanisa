from autoslug import AutoSlugField
from datetime import date
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class PublishedPostManager(models.Manager):
    def get_query_set(self):
        return super(
            PublishedPostManager,
            self).get_query_set().filter(
                publish_date__lte=date.today()
            )


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    publish_date = models.DateField()
    updated_date = models.DateTimeField(auto_now=True)
    teaser_text = models.TextField(verbose_name='Teaser')
    main_text = models.TextField(verbose_name='Main text')

    objects = models.Manager()
    published_objects = PublishedPostManager()

    def __unicode__(self):
        return self.title

    def published(self):
        return self.publish_date <= date.today()

    def get_absolute_url(self):
        return reverse(
            'kanisa_public_blog_detail',
            args=[self.publish_date.year, self.slug, ]
        )

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ['-publish_date', '-pk']
        permissions = (
            ('manage_blog',
             'Can manage your blog posts'),
        )
