from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class NavigationElement(MPTTModel):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=30,
                                   help_text=('This will be displayed on '
                                              'mouseover, so should describe '
                                              'the linked to page in a few '
                                              'words.'))
    url = models.CharField(max_length=200,
                           verbose_name='URL',
                           help_text=('Should be specified relative to the '
                                      'domain (e.g. /sermons/, not '
                                      'http://www.example.com/sermons/).'))
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children')
    require_login = models.BooleanField(default=False,
                                        help_text=('If checked, this '
                                                   'navigation element will '
                                                   'only be shown to users '
                                                   'who are logged in.'))
    modified = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        permissions = (
            ('manage_navigation',
             'Can manage your navigation'),
            )

    def __unicode__(self):
        return self.title

    def move_down(self):
        next_sibling = self.get_next_sibling()

        if not next_sibling:
            raise NavigationElement.DoesNotExist

        self.move_to(next_sibling, 'right')

        cache.delete('kanisa_navigation')

    def move_up(self):
        previous_sibling = self.get_previous_sibling()

        if not previous_sibling:
            raise Http404
        self.move_to(previous_sibling, 'left')

        cache.delete('kanisa_navigation')

    def check_parent_status(self):
        if self.pk and self.parent:
            if self.pk == self.parent.pk:
                raise ValidationError({'parent': ['A navigation element '
                                                  'cannot be its own '
                                                  'parent.', ]})

            if self.is_ancestor_of(self.parent):
                raise ValidationError({'parent': ['Invalid parent - cyclical '
                                                  'hierarchy detected.', ]})

    def clean_fields(self, exclude=None):
        self.check_parent_status()
