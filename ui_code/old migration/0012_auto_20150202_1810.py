# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0011_auto_20150202_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 3, 18, 10, 9, 422255)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 2, 18, 10, 9, 422217)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='media',
            field=models.ForeignKey(default=None, to='ui.Media', null=True),
            preserve_default=True,
        ),
    ]
