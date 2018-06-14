from django.core.exceptions import ValidationError
from django.db import models, DEFAULT_DB_ALIAS
from kanisa.fields import KanisaAutoSlugField
from mptt.models import MPTTModel, TreeForeignKey


class Page(MPTTModel):
    title = models.CharField(max_length=60)
    slug = KanisaAutoSlugField(populate_from='title')
    lead = models.TextField(
        null=True, blank=True,
        help_text=('This should be the introductory sentence or two to the '
                   'page you\'re writing.')
    )
    contents = models.TextField(
        null=True, blank=True,
        help_text=('This will follow the lead paragraph, so don\'t repeat '
                   'information already entered there.')
    )
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

    def remove_matching_navigation_elements(self):
        from kanisa.models.navigation import NavigationElement
        url = '/' + self.get_path()

        elements = NavigationElement.objects.filter(url=url,
                                                    parent__isnull=False)

        if not elements:
            return

        for element in elements:
            element.delete()

    def delete(self, using=DEFAULT_DB_ALIAS):
        self.remove_matching_navigation_elements()
        return super(Page, self).delete(using)

    def get_navigation_description(self):
        # Page leads can be null, navigation descriptions can't
        description = self.lead or self.title
        # Navigation descriptions are limited to 30 characters
        return description[:30]

    def amend_navigation(self):
        from kanisa.models.navigation import NavigationElement

        if not self.parent:
            return

        if self.draft:
            return

        parent_url = '/' + self.parent.get_path()

        try:
            element = NavigationElement.objects.get(url=parent_url)
        except NavigationElement.DoesNotExist:
            return

        if element.parent:
            return

        description = self.get_navigation_description()
        NavigationElement.objects.create(parent=element,
                                         title=self.title,
                                         description=description,
                                         url='/' + self.get_path())

    def save(self, *args, **kwargs):
        is_new_element = self.pk is None

        super(Page, self).save(*args, **kwargs)

        if is_new_element:
            self.amend_navigation()

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

    def get_published_children(self):
        return self.get_children().filter(draft=False)

    def get_published_siblings(self):
        if not self.parent:
            return []

        return self.parent.get_published_children()

    def get_breadcrumb_trail(self):
        class Breadcrumb(object):
            def __init__(self, title, path):
                self.title = title
                self.path = path

        breadcrumbs = []
        last_path = '/'
        for p in self.get_ancestors():
            last_path = last_path + p.slug + '/'
            b = Breadcrumb(p.title, last_path)
            breadcrumbs.append(b)

        return breadcrumbs


def get_page_for_part(slug, parent, candidates):
    """Returns the page in candidates which has parent as its parent,
    and a slug matching slug, or raises Page.DoesNotExist if such a
    page does not exist.

    """

    for candidate in candidates:
        if candidate.parent_id == parent.pk and candidate.slug == slug:
            return candidate

    # We've gone through all our candidates and failed to find a
    # match, so we're done.
    raise Page.DoesNotExist


def get_page_from_path_including_drafts(path):
    # path must start and end with a slash, and have a valid slug in
    # between, which means at least 3 characters
    if len(path) <= 2:
        raise Page.DoesNotExist

    if path[0] != '/' or path[-1] != '/':
        raise Page.DoesNotExist

    parts = path[1:-1].split('/')

    root_slug = parts[0]

    try:
        parent_node = Page.objects.get(parent=None,
                                       slug=root_slug)
    except Page.DoesNotExist:
        raise Page.DoesNotExist

    # We've matched the first part of our path - that's parent_node
    parts.pop(0)

    # If we've got nothing left to match, we're done
    if not parts:
        return parent_node

    descendants = parent_node.get_descendants()

    # For each part in our path, look for a page in our list of
    # descendants where the parent is the root node, and the slug is
    # the next part of our path
    for part in parts:
        parent_node = get_page_for_part(part,
                                        parent_node,
                                        descendants)

    # If we've not hit a Page.DoesNotExist yet, then we've matched
    # every part, and parent_node is the page for the last part.
    return parent_node


def get_page_from_path(path):
    page = get_page_from_path_including_drafts(path)

    if page.draft:
        raise Page.DoesNotExist

    return page
