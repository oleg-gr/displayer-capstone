# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0006_auto_20141213_0552'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='task',
            field=models.ForeignKey(default=1, to='ui.Task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 5, 55, 56, 153216)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 5, 55, 56, 153177)),
            preserve_default=True,
        ),
    ]
