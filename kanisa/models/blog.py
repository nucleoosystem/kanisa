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
    publish_date = models.DateField(
        help_text=('Blog posts are published on the site at 00:00 on the '
                   'publish date.')
    )
    updated_date = models.DateTimeField(auto_now=True)
    teaser_text = models.TextField(
        verbose_name='Teaser',
        help_text=('This should normally be the first few sentences of your '
                   'post.')
    )
    main_text = models.TextField(
        verbose_name='Main text',
        help_text=('This should be the bulk of your post, and will follow on '
                   'from what\'s in the teaser.')
    )

    objects = models.Manager()
    published_objects = PublishedPostManager()

    def __unicode__(self):
        return self.title

    def published(self):
        return self.publish_date <= date.today()

    def full_text(self):
        return self.teaser_text + '\n\n' + self.main_text

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
