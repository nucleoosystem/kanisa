# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import kanisa.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0014_document_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='inlineimage',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='regularevent',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='sermonseries',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
        migrations.AlterField(
            model_name='sermonspeaker',
            name='slug',
            field=kanisa.fields.KanisaAutoSlugField(editable=False),
        ),
    ]
