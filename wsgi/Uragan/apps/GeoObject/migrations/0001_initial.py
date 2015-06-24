# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.TextField(unique=True, verbose_name='title geographical object')),
                ('lat', models.FloatField(verbose_name='northern latitude in degrees')),
                ('lon', models.FloatField(verbose_name='eastern longitude in degrees')),
                ('short_description', models.TextField(null=True, verbose_name='short description', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('polygon', models.TextField(null=True, verbose_name='polygon in KML format', blank=True)),
                ('color', models.CharField(null=True, max_length=20, verbose_name='color', blank=True)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='last modification')),
            ],
            options={
                'verbose_name': 'geographical object',
                'verbose_name_plural': 'geographical objects',
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('image', models.ImageField(upload_to='geo_objects/images/', verbose_name='image')),
            ],
            options={
                'verbose_name': 'geographical object image',
                'verbose_name_plural': 'images of geographical objects',
            },
        ),
        migrations.CreateModel(
            name='SurveillancePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.TextField(verbose_name='title surveillance plan')),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('time_end', models.DateTimeField(default=datetime.datetime(2015, 6, 27, 0, 54, 9, 843803, tzinfo=utc))),
                ('last_modification', models.DateTimeField(auto_now=True, verbose_name='date and time created')),
                ('geo_objects', models.ManyToManyField(verbose_name='observed objects', to='GeoObject.GeoObject')),
                ('researches', models.ManyToManyField(verbose_name='researches', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'surveillance plan',
                'verbose_name_plural': 'surveillance plans',
            },
        ),
        migrations.AddField(
            model_name='geoobject',
            name='images',
            field=models.ManyToManyField(to='GeoObject.Images', verbose_name='images of geographical object', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='geoobject',
            unique_together=set([('lat', 'lon')]),
        ),
    ]
