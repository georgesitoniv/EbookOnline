# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0003_auto_20170411_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='visits',
        ),
        migrations.RemoveField(
            model_name='book',
            name='visits',
        ),
        migrations.RemoveField(
            model_name='category',
            name='visits',
        ),
        migrations.AddField(
            model_name='author',
            name='visitors',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='visitors',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='visitors',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
