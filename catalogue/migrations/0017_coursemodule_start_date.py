# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-01 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0016_auto_20190818_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodule',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]