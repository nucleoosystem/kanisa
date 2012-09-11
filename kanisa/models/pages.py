from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    title = models.CharField(max_length=60)
    slug = AutoSlugField(populate_from='title', unique=True)
    summary = models.TextField(null=True, blank=True)
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
            if self.parent and self.parent.draft:
                msg = ('Cannot mark this page as published, as its '
                       'parent page (%s) is '
                       'currently a draft.' % self.parent)
                raise ValidationError({'draft': [msg, ]})

        if self.draft and not self.is_leaf_node():
            descendants = self.get_descendants()

            for d in descendants:
                if not d.draft:
                    msg = ('Cannot mark this page as draft, as it has '
                           'published descendants.')
                    raise ValidationError({'draft': [msg, ]})

    def clean_fields(self, exclude=None):
        self.check_parent_status()
        self.check_draft_status()

    def get_path(self):
        ancestors_path = [p.slug for p in self.get_ancestors()]
        ancestors_path.append(self.slug)
        return '/'.join(ancestors_path) + '/'


def get_page_from_path(path):
    # path must start and end with a slash, and have a valid slug in
    # between, which means at least 3 characters
    if len(path) <= 2:
        raise Page.DoesNotExist

    if path[0] != '/' or path[-1] != '/':
        raise Page.DoesNotExist

    parts = path[1:-1].split('/')

    root_slug = parts[0]

    try:
        root_node = Page.objects.get(parent=None,
                                     slug=root_slug,
                                     draft=False)
    except Page.DoesNotExist:
        raise Page.DoesNotExist

    # If we've only got a single slug in our path, we're done
    if len(parts) == 1:
        return root_node

    descendants = root_node.get_descendants()
    descendants = [d for d in descendants if not d.draft]

    # Look for a page in our list of descendants where the parent is
    # the root node, and the slug is the next part of our path
    parent_node = root_node

    for part in parts[1:]:
        this_part = None

        for descendant in descendants:
            # If the descendant we're looking at does not have a
            # parent matching the last part we matched, it's not
            # relevant at this stage.
            if descendant.parent_id != parent_node.pk:
                continue

            # If slug of the descendant we're looking at does not
            # match the path we're looking at, it's not relevant
            if descendant.slug == part:
                parent_node = descendant
                this_part = descendant

        # If we've not found a match for this part, we've not found a
        # match for the whole thing.
        if not this_part:
            raise Page.DoesNotExist

    # If we've not hit a Page.DoesNotExist yet, then we've matched
    # every part, and this_part is the page for the last part.
    return this_part
