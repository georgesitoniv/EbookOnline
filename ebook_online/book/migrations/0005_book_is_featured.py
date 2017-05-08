# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_auto_20170411_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
