from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    title = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='title', unique=True)
    contents = models.TextField(null=True, blank=True)
    draft = models.BooleanField(default=False)
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children')
    modified = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['slug']

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_pages',
             'Can manage your pages'),
            )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)
        from haystack import site as haystack_site
        haystack_site.get_index(self.__class__).update_object(self)

    def check_parent_status(self):
        if self.pk and self.parent:
            if self.pk == self.parent.pk:
                raise ValidationError({'parent': ['A page cannot be its own '
                                                  'parent.', ]})

            if self.is_ancestor_of(self.parent):
                raise ValidationError({'parent': ['Invalid parent - cyclical '
                                                  'hierarchy detected.', ]})

    def check_draft_status(self):
        if not self.draft:
            ancestors = self.get_ancestors()
            for a in ancestors:
                if a.draft:
                    raise ValidationError({'draft': ['Cannot mark this page '
                                                     'as published, as it has '
                                                     'non-published '
                                                     'ancestors.', ]})

        if self.draft and not self.is_leaf_node():
            descendants = self.get_descendants()

            for d in descendants:
                if not d.draft:
                    raise ValidationError({'draft': ['Cannot mark this page '
                                                     'as draft, as it has '
                                                     'published '
                                                     'descendants.', ]})

    def clean_fields(self, exclude=None):
        self.check_parent_status()
        self.check_draft_status()
