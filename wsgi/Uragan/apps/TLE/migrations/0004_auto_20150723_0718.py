# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('TLE', '0003_subsattellitepoints'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubsatellitePoint',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='date and time')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, geography=True, verbose_name='subsatellite point location')),
                ('tle', models.ForeignKey(to='TLE.TLE')),
            ],
            options={
                'verbose_name_plural': 'subsatellite points',
                'ordering': ('-date_time',),
                'verbose_name': 'subsatellite point',
            },
        ),
        migrations.RemoveField(
            model_name='subsattellitepoints',
            name='satellite',
        ),
        migrations.DeleteModel(
            name='SubsattellitePoints',
        ),
    ]
