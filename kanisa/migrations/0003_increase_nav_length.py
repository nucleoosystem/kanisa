# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0002_registereduser_is_spam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navigationelement',
            name='alternate_title',
            field=models.CharField(help_text=b'This will be used where the link is the root link, as the text for the link itself (as opposed to the dropdown menu title).', max_length=40, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='navigationelement',
            name='title',
            field=models.CharField(max_length=40),
            preserve_default=True,
        ),
    ]
