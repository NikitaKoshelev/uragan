# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeoObject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='title geographical object')),
                ('lat', models.FloatField(verbose_name='latitude in degrees')),
                ('lon', models.FloatField(verbose_name='longitude in degrees')),
                ('short_description', models.TextField(verbose_name='short description')),
                ('description', models.TextField(verbose_name='description')),
                ('polygon', models.TextField(null=True, verbose_name='polygon in KML format')),
                ('color', models.TextField(null=True, verbose_name='color')),
            ],
            options={
                'verbose_name_plural': 'geographical objects',
                'verbose_name': 'geographical object',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('image', models.ImageField(upload_to='geo_objects', verbose_name='image')),
            ],
            options={
                'verbose_name_plural': 'images of geographical objects',
                'verbose_name': 'geographical object image',
            },
        ),
        migrations.CreateModel(
            name='SurveillancePlan',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('time_start', models.DateTimeField(auto_now=True)),
                ('time_end', models.DateTimeField(default=datetime.datetime(2015, 5, 16, 0, 47, 53, 792337, tzinfo=utc))),
                ('geo_objects', models.ManyToManyField(to='GeoObject.GeoObject', verbose_name='observed objects')),
            ],
            options={
                'verbose_name_plural': 'surveillance plans',
                'verbose_name': 'surveillance plan',
            },
        ),
    ]
