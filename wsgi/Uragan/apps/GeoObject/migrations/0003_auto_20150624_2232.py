# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GeoObject', '0002_auto_20150624_0359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='geoobject',
            options={'verbose_name_plural': 'geographical objects', 'ordering': ('title',), 'verbose_name': 'geographical object'},
        ),
        migrations.AlterField(
            model_name='geoobject',
            name='color',
            field=models.CharField(default='#0000ff', max_length=20, null=True, blank=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='surveillanceplan',
            name='time_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 27, 19, 32, 28, 963369, tzinfo=utc)),
        ),
    ]
