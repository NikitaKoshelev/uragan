# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 0, 13, 18, 274949, tzinfo=utc), verbose_name='date and time end'),
        ),
    ]
