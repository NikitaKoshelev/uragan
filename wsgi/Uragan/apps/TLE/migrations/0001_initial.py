# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='satellite title')),
                ('satellite_number', models.IntegerField(unique=True, verbose_name='number of satellites in the database NORAD')),
                ('about_satellite', models.TextField(null=True, verbose_name='about satellite')),
                ('image', models.ImageField(upload_to='satellites', null=True, verbose_name='satellite image')),
            ],
            options={
                'db_table': 'Satellites',
                'verbose_name_plural': 'satellites',
                'verbose_name': 'satellite',
            },
        ),
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='date and time of creation')),
                ('title_line', models.CharField(max_length=24, verbose_name='title in line two-line element set')),
                ('line1', models.CharField(max_length=69, verbose_name='first line in two-line element set')),
                ('line2', models.CharField(max_length=69, verbose_name='second line in two-line element set')),
                ('datetime_in_lines', models.DateTimeField(blank=True, verbose_name='date and time in two-line element set')),
                ('satellite', models.ForeignKey(to='TLE.Satellite', to_field='satellite_number')),
            ],
            options={
                'db_table': 'TLE',
                'ordering': ['-datetime_in_lines'],
                'get_latest_by': 'datetime_in_lines',
                'verbose_name': 'two-line element set',
                'verbose_name_plural': 'two-line element sets',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tle',
            unique_together=set([('datetime_in_lines', 'satellite')]),
        ),
    ]
