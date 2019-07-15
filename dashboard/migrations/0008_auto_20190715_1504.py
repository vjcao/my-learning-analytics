# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-15 19:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20190626_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('resource_type', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Resource Type')),
                ('id', models.CharField(max_length=255, primary_key=True, verbose_name='Resource Id')),
                ('name', models.TextField(verbose_name='Resource Name')),
                ('course_id', models.BigIntegerField(verbose_name='Course Id')),
            ],
            options={
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='ResourceAccess',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Table Id')),
                ('resource_id', models.CharField(blank=True, max_length=255, verbose_name='Resource Id')),
                ('user_id', models.BigIntegerField(blank=True, verbose_name='User Id')),
                ('access_time', models.DateTimeField(verbose_name='Access Time')),
            ],
            options={
                'db_table': 'resource_access',
            },
        ),
        migrations.DeleteModel(
            name='File',
        ),
        migrations.DeleteModel(
            name='FileAccess',
        ),
        migrations.RemoveField(
            model_name='courseviewoption',
            name='show_files_accessed',
        ),
        migrations.AddField(
            model_name='courseviewoption',
            name='show_resources_accessed',
            field=models.BooleanField(default=True, verbose_name='Show Resources Accessed View'),
        ),
    ]
