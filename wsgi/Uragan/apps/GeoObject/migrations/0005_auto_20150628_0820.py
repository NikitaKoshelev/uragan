# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0004_auto_20150628_0535'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveillanceplan',
            name='creation_datetime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 6, 28, 5, 20, 48, 34307, tzinfo=utc), verbose_name='creation date and time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='last_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='researchers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='researchers'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 5, 20, 28, 826682, tzinfo=utc), verbose_name='date and time end'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_start',
            field=models.DateTimeField(auto_now=True, verbose_name='date and time start'),
        ),
    ]
