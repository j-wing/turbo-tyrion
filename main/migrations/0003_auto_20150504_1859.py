# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150504_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graphscore',
            name='output_filename',
        ),
        migrations.AddField(
            model_name='graphscore',
            name='output_file',
            field=models.FileField(null=True, upload_to=main.models.get_output_name, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inputgraph',
            name='input_filename',
            field=models.FilePathField(path=b'/media/jordonwii/apps/nptsp_leaders/tests/inputs', max_length=255),
            preserve_default=True,
        ),
    ]
