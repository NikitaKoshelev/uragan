# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GeoObject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveillanceplan',
            name='researches',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='researches'),
        ),
        migrations.AddField(
            model_name='images',
            name='geo_object',
            field=models.ForeignKey(to='GeoObject.GeoObject', verbose_name='geographical object'),
        ),
        migrations.AlterUniqueTogether(
            name='geoobject',
            unique_together=set([('lat', 'lon')]),
        ),
    ]
