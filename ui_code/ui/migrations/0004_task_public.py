# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0003_displayeruser_schedule_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
