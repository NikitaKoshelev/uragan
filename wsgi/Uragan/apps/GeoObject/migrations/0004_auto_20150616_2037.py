# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0003_auto_20150513_1319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='images',
            name='geo_object',
        ),
        migrations.AddField(
            model_name='geoobject',
            name='images',
            field=models.ManyToManyField(blank=True, to='GeoObject.Images', verbose_name='images of geographical object'),
        ),
        migrations.AddField(
            model_name='images',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='images',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title', default=datetime.datetime(2015, 6, 16, 20, 37, 41, 401087, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='color',
            field=models.TextField(blank=True, null=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='lat',
            field=models.FloatField(verbose_name='northern latitude in degrees'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='lon',
            field=models.FloatField(verbose_name='eastern longitude in degrees'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='polygon',
            field=models.TextField(blank=True, null=True, verbose_name='polygon in KML format'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='short description'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 19, 20, 35, 51, 42552, tzinfo=utc)),
        ),
    ]
