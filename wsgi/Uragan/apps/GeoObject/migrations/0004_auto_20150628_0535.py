# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0003_auto_20150624_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveillanceplan',
            name='description',
            field=models.TextField(verbose_name='description', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='surveillanceplan',
            name='short_description',
            field=models.TextField(verbose_name='short description', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 1, 2, 35, 7, 511453, tzinfo=utc)),
        ),
    ]
