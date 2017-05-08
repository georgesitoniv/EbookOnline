# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170411_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follow',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
