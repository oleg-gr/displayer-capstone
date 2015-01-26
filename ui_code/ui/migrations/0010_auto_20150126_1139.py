# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0009_auto_20150124_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='display',
            name='id',
        ),
        migrations.RemoveField(
            model_name='displayeruser',
            name='id',
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.ForeignKey(default=1, to='ui.Capability'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='display',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='displayeruser',
            name='user',
            field=models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 27, 11, 39, 16, 31389)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 26, 11, 39, 16, 31356)),
            preserve_default=True,
        ),
    ]
