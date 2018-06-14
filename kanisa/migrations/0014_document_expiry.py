# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0013_remove_document_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='expiry_months',
            field=models.IntegerField(default=0, verbose_name=b'Expires after', choices=[(0, b'Never'), (6, b'6 months'), (12, b'1 year'), (24, b'2 years'), (60, b'5 years')]),
        ),
    ]
