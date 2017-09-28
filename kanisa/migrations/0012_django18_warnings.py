# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0011_django18'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regularevent',
            name='categories',
            field=models.ManyToManyField(to='kanisa.EventCategory', verbose_name=b'Event Categories', blank=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='event',
            field=models.OneToOneField(to='kanisa.ScheduledEvent'),
        ),
    ]
