# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import filer.fields.image
import djangocms_text_ckeditor.fields
import django.db.models.deletion
from django.conf import settings
import django.core.validators
import autoslug.autoslugmixin


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('description', djangocms_text_ckeditor.fields.HTMLField(max_length=2000, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
                ('display_image', filer.fields.image.FilerImageField(related_name='author_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'display image', blank=True, to='filer.Image', null=True)),
            ],
            bases=(autoslug.autoslugmixin.AutoUniqueSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('year_published', models.DateField()),
                ('date_posted', models.DateField(auto_now=True)),
                ('description', djangocms_text_ckeditor.fields.HTMLField(max_length=3000, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
                ('author', models.ForeignKey(to='book.Author')),
            ],
            bases=(autoslug.autoslugmixin.AutoUniqueSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BookShelf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('books', models.ManyToManyField(to='book.Book')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
                ('display_image', filer.fields.image.FilerImageField(related_name='category_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'display image', blank=True, to='filer.Image', null=True)),
            ],
            bases=(autoslug.autoslugmixin.AutoUniqueSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review_content', models.CharField(max_length=1000)),
                ('date_posted', models.DateField(auto_now=True)),
                ('book', models.ForeignKey(to='book.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(to='book.Category', blank=True),
        ),
        migrations.AddField(
            model_name='book',
            name='display_image',
            field=filer.fields.image.FilerImageField(related_name='book_image', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'display image', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='ebook_file',
            field=filer.fields.file.FilerFileField(related_name='ebook_file', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'file', blank=True, to='filer.File', null=True),
        ),
    ]
