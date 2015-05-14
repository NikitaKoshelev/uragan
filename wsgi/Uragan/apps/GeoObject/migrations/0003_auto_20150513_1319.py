# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0002_auto_20150513_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 16, 13, 19, 32, 137494, tzinfo=utc)),
        ),
    ]
