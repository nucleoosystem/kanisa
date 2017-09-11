# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0007_sitewidenotice_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='regularevent',
            name='mothballed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
