# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0012_django18_warnings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='public',
        ),
    ]
