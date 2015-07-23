# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoObject',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.TextField(unique=True, verbose_name='title geographical object')),
                ('lat', models.FloatField(verbose_name='northern latitude in degrees')),
                ('lon', models.FloatField(verbose_name='eastern longitude in degrees')),
                ('short_description', models.TextField(null=True, verbose_name='short description', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, verbose_name='geometry in KML format', blank=True)),
                ('color', models.CharField(default='#0000ff', null=True, blank=True, verbose_name='color', max_length=20)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'geographical object',
                'verbose_name_plural': 'geographical objects',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.TextField(verbose_name='title surveillance plan')),
                ('short_description', models.TextField(null=True, verbose_name='short description', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('time_start', models.DateTimeField(auto_now=True, verbose_name='date and time start')),
                ('time_end', models.DateTimeField(default=datetime.datetime(2015, 7, 26, 8, 0, 4, 853275, tzinfo=utc), verbose_name='date and time end')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation date and time')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='modification date and time')),
                ('geo_objects', models.ManyToManyField(to='GeoObject.GeoObject', verbose_name='observed objects')),
                ('researchers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='researchers', blank=True)),
            ],
            options={
                'verbose_name': 'surveillance plan',
                'verbose_name_plural': 'surveillance plans',
            },
        ),
        migrations.AddField(
            model_name='geoobject',
            name='images',
            field=models.ManyToManyField(to='GeoObject.Images', null=True, verbose_name='images of geographical object', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='geoobject',
            unique_together=set([('lat', 'lon')]),
        ),
    ]
