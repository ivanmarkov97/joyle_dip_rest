# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 13:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delegate_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delegation',
            old_name='recipient',
            new_name='owner',
        ),
    ]