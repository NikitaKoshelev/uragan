# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0003_auto_20150723_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(verbose_name='date and time end', default=datetime.datetime(2015, 7, 26, 1, 6, 35, 208648, tzinfo=utc)),
        ),
    ]
