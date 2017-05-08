# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('account', '0006_remove_userprofile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='display_image',
            field=filer.fields.image.FilerImageField(related_name='user_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'display image', blank=True, to='filer.Image', null=True),
        ),
    ]
