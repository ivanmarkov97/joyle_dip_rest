# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='projectgroup',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='relation',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
