# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0002_auto_20150723_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 26, 1, 6, 22, 898409, tzinfo=utc), verbose_name='date and time end'),
        ),
    ]
