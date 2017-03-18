# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200, verbose_name='satellite title')),
                ('satellite_number', models.IntegerField(unique=True, verbose_name='number of satellites in the database NORAD')),
                ('about_satellite', models.TextField(null=True, verbose_name='about satellite')),
                ('image', models.ImageField(null=True, verbose_name='satellite image', upload_to='satellites')),
            ],
            options={
                'db_table': 'Satellites',
                'verbose_name': 'satellite',
                'verbose_name_plural': 'satellites',
            },
        ),
        migrations.CreateModel(
            name='SubsatellitePoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date_time', models.DateTimeField(verbose_name='date and time')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='subsatellite point location', geography=True)),
            ],
            options={
                'ordering': ('-date_time',),
                'verbose_name': 'subsatellite point',
                'verbose_name_plural': 'subsatellite points',
            },
        ),
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date and time of creation')),
                ('title_line', models.CharField(max_length=24, verbose_name='title in line two-line element set')),
                ('line1', models.CharField(max_length=69, verbose_name='first line in two-line element set')),
                ('line2', models.CharField(max_length=69, verbose_name='second line in two-line element set')),
                ('datetime_in_lines', models.DateTimeField(verbose_name='date and time in two-line element set', blank=True)),
                ('satellite', models.ForeignKey(to='TLE.Satellite', to_field='satellite_number')),
            ],
            options={
                'db_table': 'TLE',
                'verbose_name': 'two-line element set',
                'verbose_name_plural': 'two-line element sets',
                'ordering': ['-datetime_in_lines'],
                'get_latest_by': 'datetime_in_lines',
            },
        ),
        migrations.AddField(
            model_name='subsatellitepoint',
            name='tle',
            field=models.ForeignKey(to='TLE.TLE'),
        ),
        migrations.AlterUniqueTogether(
            name='tle',
            unique_together=set([('datetime_in_lines', 'satellite')]),
        ),
    ]
