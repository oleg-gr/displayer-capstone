# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0010_auto_20150126_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media', models.FileField(upload_to=b'')),
            ],
            options={
                'db_table': 'displayer_media',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='media',
            field=models.ForeignKey(default=None, to='ui.Media', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 3, 18, 11, 32, 283518)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2015, 2, 2, 18, 11, 32, 283481)),
            preserve_default=True,
        ),
    ]
