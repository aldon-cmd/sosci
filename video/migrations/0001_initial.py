# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-04 19:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogue', '0014_auto_20190804_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('video_id', models.IntegerField()),
                ('seen', models.BooleanField(default=False, help_text='determines whether a video has been watched or not')),
                ('width', models.IntegerField(default=800)),
                ('height', models.IntegerField(default=480)),
                ('duration', models.DecimalField(decimal_places=2, default=0, help_text='duration of the video', max_digits=64)),
                ('picture', models.CharField(blank=True, help_text='a url pointing directly to a preview image of the video', max_length=250, null=True)),
                ('upload_link', models.CharField(blank=True, help_text='a link that points directly to the video on the vimeo server', max_length=250, null=True)),
                ('upload_status', models.CharField(blank=True, help_text='the upload status of the video. possible values are: in_progress, complete, error', max_length=11, null=True)),
                ('transcode_status', models.CharField(blank=True, help_text='the transcoding status of the video. possible values are: in_progress, complete, error', max_length=11, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='catalogue.Product')),
            ],
        ),
    ]
