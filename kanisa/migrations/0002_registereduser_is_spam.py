# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registereduser',
            name='is_spam',
            field=models.BooleanField(default=False, help_text=b'Hides this user from management screens'),
            preserve_default=True,
        ),
    ]
