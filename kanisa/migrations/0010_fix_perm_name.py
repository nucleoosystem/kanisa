# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_perm_name(apps, schema_editor):
    Permission = apps.get_model(
        'auth',
        'Permission'
    )
    try:
        perm = Permission.objects.get(codename='manage_sitewidenotices')
        perm.name = 'Can manage your site wide notices'
        perm.save()
    except Permission.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('kanisa', '0009_sitewidenotice_perms'),
    ]

    operations = [
        migrations.RunPython(fix_perm_name)
    ]
