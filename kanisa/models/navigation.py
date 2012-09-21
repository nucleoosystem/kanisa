from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class NavigationElement(MPTTModel):
    title = models.CharField(max_length=20)
    url = models.CharField(max_length=200,
                           verbose_name='URL',
                           help_text=('Should be specified relative to the '
                                      'domain (e.g. /sermons/, not '
                                      'http://www.example.com/sermons/).'))
    parent = TreeForeignKey('self',
                            null=True,
                            blank=True,
                            related_name='children')
    require_login = models.BooleanField(default=False)
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

    def check_parent_status(self):
        if self.pk and self.parent:
            if self.pk == self.parent.pk:
                raise ValidationError({'parent': ['A page cannot be its own '
                                                  'parent.', ]})

            if self.is_ancestor_of(self.parent):
                raise ValidationError({'parent': ['Invalid parent - cyclical '
                                                  'hierarchy detected.', ]})

    def clean_fields(self, exclude=None):
        self.check_parent_status()
