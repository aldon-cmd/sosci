# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-15 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livestream', '0003_auto_20190915_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='twilioroom',
            name='end_time',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]