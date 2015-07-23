# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0006_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geoobject',
            name='polygon',
        ),
        migrations.AddField(
            model_name='geoobject',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='geometry in KML format'),
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='images',
            field=models.ManyToManyField(blank=True, to='GeoObject.Images', null=True, verbose_name='images of geographical object'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 4, 18, 28, 652696, tzinfo=utc), verbose_name='date and time end'),
        ),
    ]
