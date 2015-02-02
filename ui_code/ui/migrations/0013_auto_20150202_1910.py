# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0012_auto_20150202_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='media',
        ),
        migrations.AddField(
            model_name='media',
            name='task',
            field=models.ForeignKey(default=1, to='ui.Task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 3, 19, 10, 15, 60707)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 2, 19, 10, 15, 60672)),
            preserve_default=True,
        ),
    ]
