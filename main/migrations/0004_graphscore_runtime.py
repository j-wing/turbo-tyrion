# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150504_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphscore',
            name='runtime',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
