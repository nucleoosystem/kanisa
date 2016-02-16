# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0005_delete_scheduledtweet'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteWideNotice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(help_text=b'Keep this short, summarise your announcement in a few words.', max_length=60)),
                ('contents', models.TextField(help_text=b'This should be a few sentences at most.')),
                ('created', models.DateField(auto_now_add=True)),
                ('publish_until', models.DateField(help_text=b'The last date on which your notice will be visible.')),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-publish_until',),
                'permissions': (('manage_banners', 'Can manage your banners'),),
            },
            bases=(models.Model,),
        ),
    ]
