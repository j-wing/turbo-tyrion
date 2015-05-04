# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphscore',
            name='output_filename',
            field=models.FilePathField(max_length=255, path=b'/media/jordonwii/apps/nptsp_leaders/main/outputs', null=True, blank=True),
            preserve_default=True,
        ),
    ]
