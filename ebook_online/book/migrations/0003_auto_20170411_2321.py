# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20170411_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='visits',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='visits',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='visits',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
