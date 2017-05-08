# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20170414_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='display_image',
            field=models.ImageField(null=True, upload_to=b'users/%Y/%m/%d', blank=True),
        ),
    ]
