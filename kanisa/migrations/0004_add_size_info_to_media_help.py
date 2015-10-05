# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0003_increase_nav_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inlineimage',
            name='image',
            field=sorl.thumbnail.fields.ImageField(help_text=b'Image will be: <ul><li>960x200px for headline images (the image will be cropped to fit);</li><li>260x260px for medium images (resized without cropping);</li><li>174x174px for small images (resized without cropping).</li></ul>', upload_to=b'kanisa/media/'),
            preserve_default=True,
        ),
    ]
