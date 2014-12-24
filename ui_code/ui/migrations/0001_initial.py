# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Capability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'displayer_capability',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capabilities', models.ManyToManyField(to='ui.Capability')),
            ],
            options={
                'db_table': 'displayer_display',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'displayer_location',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='display',
            name='location',
            field=models.ForeignKey(to='ui.Location'),
            preserve_default=True,
        ),
    ]
