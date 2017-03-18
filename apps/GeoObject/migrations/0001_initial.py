# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoObject',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('color', models.CharField(verbose_name='color', blank=True, null=True, default='#0000ff', max_length=20)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('description', models.TextField(verbose_name='description', blank=True, null=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(verbose_name='geometry in KML format', blank=True, srid=4326, null=True)),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification')),
                ('lat', models.FloatField(verbose_name='northern latitude in degrees')),
                ('location', django.contrib.gis.db.models.fields.PointField(verbose_name='location point', geography=True, srid=4326, unique=True)),
                ('lon', models.FloatField(verbose_name='eastern longitude in degrees')),
                ('short_description', models.TextField(verbose_name='short description', blank=True, null=True)),
                ('title', models.TextField(verbose_name='title geographical object', db_index=True, unique=True)),
            ],
            options={
                'verbose_name': 'geographical object',
                'verbose_name_plural': 'geographical objects',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('description', models.TextField(verbose_name='description', blank=True, null=True)),
                ('image', models.ImageField(verbose_name='image', upload_to='geo_objects/images/')),
            ],
            options={
                'verbose_name': 'geographical object image',
                'verbose_name_plural': 'images of geographical objects',
            },
        ),
        migrations.CreateModel(
            name='SurveillancePlan',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.TextField(verbose_name='title surveillance plan')),
                ('short_description', models.TextField(verbose_name='short description', blank=True, null=True)),
                ('description', models.TextField(verbose_name='description', blank=True, null=True)),
                ('time_start', models.DateTimeField(auto_now=True, verbose_name='date and time start')),
                ('time_end', models.DateTimeField(verbose_name='date and time end', default=datetime.datetime(2015, 8, 12, 20, 49, 4, 283217, tzinfo=utc))),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation date and time')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='modification date and time')),
                ('geo_objects', models.ManyToManyField(verbose_name='observed objects', to='GeoObject.GeoObject')),
                ('researchers', models.ManyToManyField(verbose_name='researchers', blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'surveillance plan',
                'verbose_name_plural': 'surveillance plans',
            },
        ),
        migrations.AddField(
            model_name='geoobject',
            name='images',
            field=models.ManyToManyField(verbose_name='images of geographical object', blank=True, to='GeoObject.Images'),
        ),
    ]
