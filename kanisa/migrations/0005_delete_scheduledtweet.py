# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0004_add_size_info_to_media_help'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ScheduledTweet',
        ),
    ]
