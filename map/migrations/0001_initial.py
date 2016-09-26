# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-24 01:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('external_identifier', models.CharField(max_length=255)),
                ('area_type', models.CharField(choices=[('UNCATEGORIZED', 'Uncategorized'), ('NEIGHBORHOOD', 'Neighborhood'), ('WARD', 'Ward'), ('STATE', 'State'), ('COUNTRY', 'Country'), ('REGION', 'Region'), ('COUNTY', 'County')], max_length=50)),
                ('boundary_type', models.CharField(choices=[('OUTER', 'Outer Boundary'), ('INNER', 'Inner Boundary')], max_length=50)),
                ('polygon', models.TextField()),
                ('mbr', models.CharField(max_length=255)),
                ('created_time', models.DateTimeField()),
                ('outer_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inner_area', to='map.Area')),
            ],
        ),
        migrations.CreateModel(
            name='AreaMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dataset_identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('kml_file', models.FileField(blank=True, null=True, upload_to='uploads/areamap/')),
                ('created_time', models.DateTimeField()),
                ('areas', models.ManyToManyField(to='map.Area')),
            ],
        ),
        migrations.CreateModel(
            name='KmlMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('kml_file', models.FileField(upload_to='uploads/datamap/')),
                ('created_time', models.DateTimeField()),
                ('updated_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
