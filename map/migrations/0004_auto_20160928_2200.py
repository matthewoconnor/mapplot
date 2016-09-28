# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 22:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_auto_20160928_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='is_primary',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='area',
            name='primary_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_areas', related_query_name='child_area', to='map.Area'),
        ),
        migrations.AlterField(
            model_name='area',
            name='outer_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inner_areas', related_query_name='inner_area', to='map.Area'),
        ),
    ]
