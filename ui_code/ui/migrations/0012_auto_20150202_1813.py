# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0011_auto_20150202_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='media',
            options={'verbose_name_plural': 'media'},
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 3, 18, 13, 37, 791272)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 2, 18, 13, 37, 791244)),
            preserve_default=True,
        ),
    ]
