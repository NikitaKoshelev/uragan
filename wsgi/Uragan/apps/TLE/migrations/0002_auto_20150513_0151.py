# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TLE', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tle',
            name='datetime_created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='date and time of creation'),
        ),
    ]
