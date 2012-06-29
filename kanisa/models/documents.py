from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=60,
                             help_text='The name of the document.')
    file = models.FileField(upload_to='kanisa/documents')
    details = models.TextField(blank=True,
                               null=True,
                               help_text=('Give a brief idea of what\'s in '
                                          'this document.'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        # Need this because I've split up models.py into multiple
        # files.
        app_label = 'kanisa'
        ordering = ('-modified', )
