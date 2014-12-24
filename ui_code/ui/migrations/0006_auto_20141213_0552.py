# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0005_auto_20141213_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 14, 5, 52, 43, 773221)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 5, 52, 43, 773186)),
            preserve_default=True,
        ),
    ]
