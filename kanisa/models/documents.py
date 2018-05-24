from autoslug import AutoSlugField
import datetime
from django.core.urlresolvers import reverse
from django.db import models
import os


KNOWN_EXTENSIONS = {
    '.doc': 'Word Document',
    '.docx': 'Word Document',
    '.pdf': 'PDF',
    '.xls': 'Excel Document',
    '.xlxs': 'Excel Document',
}


class Document(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the document.')
    slug = AutoSlugField(populate_from='title', unique=True)
    file = models.FileField(upload_to='kanisa/documents')
    details = models.TextField(
        blank=True,
        null=True,
        help_text=('Give a brief idea of what\'s in '
                   'this document.')
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    downloads = models.IntegerField(
        default=0,
        editable=False
    )

    def __unicode__(self):
        return self.title

    def file_name(self):
        return os.path.basename(self.file.name)

    def extension_description(self):
        prefix, extension = os.path.splitext(self.file.name)

        extension = extension.lower()
        return KNOWN_EXTENSIONS.get(extension, extension)

    def download_url(self):
        return reverse('kanisa_members_documents_download', args=[self.pk, ])

    def likely_revised(self):
        modification_delta = self.modified - self.created
        return modification_delta > datetime.timedelta(hours=1)

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-created', )
        permissions = (
            ('manage_documents',
             'Can manage your documents'),
        )
