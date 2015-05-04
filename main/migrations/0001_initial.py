# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('command', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GraphScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_cost', models.IntegerField()),
                ('path', models.TextField()),
                ('output_filename', models.FilePathField(path=b'/media/jordonwii/apps/nptsp_leaders/main/outputs', max_length=255)),
                ('algo', models.ForeignKey(to='main.Algorithm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InputGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('input_filename', models.FilePathField(path=b'/media/jordonwii/apps/nptsp_leaders/main/inputs', max_length=255)),
                ('last_run_start', models.DateTimeField(null=True, blank=True)),
                ('last_run_end', models.DateTimeField(null=True, blank=True)),
                ('is_test_graph', models.BooleanField(default=False)),
                ('current_best', models.ForeignKey(blank=True, to='main.GraphScore', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='graphscore',
            name='graph',
            field=models.ForeignKey(to='main.InputGraph'),
            preserve_default=True,
        ),
    ]
