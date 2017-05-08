# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_auto_20170412_0119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='year_published',
            new_name='date_published',
        ),
    ]
