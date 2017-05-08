# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_book_is_featured'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RenameField(
            model_name='author',
            old_name='visitors',
            new_name='visitor',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='visitors',
            new_name='visitor',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='visitors',
            new_name='visitor',
        ),
    ]
