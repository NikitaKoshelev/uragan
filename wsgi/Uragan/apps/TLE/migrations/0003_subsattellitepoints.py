# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TLE', '0002_auto_20150513_0151'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubsattellitePoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('datetime', models.DateTimeField(verbose_name='date and time')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, verbose_name='subsatellite point location')),
                ('satellite', models.ForeignKey(to='TLE.Satellite')),
            ],
            options={
                'ordering': ('-datetime',),
                'verbose_name': 'subsatellite point',
                'verbose_name_plural': 'subsatellite points',
            },
        ),
    ]
