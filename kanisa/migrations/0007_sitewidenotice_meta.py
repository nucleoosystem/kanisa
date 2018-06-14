# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0006_sitewidenotice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitewidenotice',
            options={'ordering': ('-publish_until',), 'permissions': (('manage_sitewidenotices', 'Can manage your banners'),)},
        ),
    ]
