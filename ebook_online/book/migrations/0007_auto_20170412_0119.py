# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0006_auto_20170412_0116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='visitor',
        ),
        migrations.RemoveField(
            model_name='book',
            name='visitor',
        ),
        migrations.RemoveField(
            model_name='category',
            name='visitor',
        ),
        migrations.AddField(
            model_name='author',
            name='visitors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='visitors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='visitors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
