import datetime
from dateutil import relativedelta
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from kanisa.fields import KanisaAutoSlugField
import os


KNOWN_EXTENSIONS = {
    '.doc': 'Word Document',
    '.docx': 'Word Document',
    '.pdf': 'PDF',
    '.xls': 'Excel Document',
    '.xlxs': 'Excel Document',
}


class Document(models.Model):
    EXPIRY_CHOICES = (
        (0, 'Never'),
        (6, '6 months'),
        (12, '1 year'),
        (24, '2 years'),
        (60, '5 years'),
    )
    title = models.CharField(max_length=60,
                             help_text='The name of the document.')
    slug = KanisaAutoSlugField(populate_from='title')
    file = models.FileField(upload_to='kanisa/documents')
    details = models.TextField(
        blank=True,
        null=True,
        help_text=('Give a brief idea of what\'s in '
                   'this document.')
    )
    expiry_months = models.IntegerField(
        choices=EXPIRY_CHOICES,
        default=0,
        verbose_name='Expires after',
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    expired = models.BooleanField(default=False)
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

    def auto_expiry_time(self):
        if self.expiry_months == 0:
            return None

        expiry_delta = relativedelta.relativedelta(months=self.expiry_months)
        return self.modified + expiry_delta

    def has_expired(self):
        expiry_time = self.auto_expiry_time()
        if expiry_time is not None and expiry_time < now():
            self.expired = True
            self.save()

        return self.expired
    has_expired.boolean = True

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-created', )
        permissions = (
            ('manage_documents',
             'Can manage your documents'),
        )
