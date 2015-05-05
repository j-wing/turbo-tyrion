# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_graphscore_runtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputgraph',
            name='num_vars',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
