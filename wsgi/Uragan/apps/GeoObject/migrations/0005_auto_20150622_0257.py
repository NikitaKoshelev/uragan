# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0004_auto_20150616_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoobject',
            name='color',
            field=models.CharField(blank=True, max_length=20, verbose_name='color', null=True),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='title',
            field=models.TextField(unique=True, verbose_name='title geographical object'),
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(upload_to='geo_objects/images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 24, 23, 57, 19, 654726, tzinfo=utc)),
        ),
    ]
