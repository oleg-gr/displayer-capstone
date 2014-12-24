# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_task_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 5, 47, 15, 24468)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 5, 47, 15, 24441)),
            preserve_default=True,
        ),
    ]
