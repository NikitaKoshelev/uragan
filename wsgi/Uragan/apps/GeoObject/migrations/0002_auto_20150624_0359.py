# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('GeoObject', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveillanceplan',
            name='researches',
        ),
        migrations.AddField(
            model_name='surveillanceplan',
            name='researchers',
            field=models.ManyToManyField(verbose_name='researchers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 27, 0, 59, 28, 61864, tzinfo=utc)),
        ),
    ]
