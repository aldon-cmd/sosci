# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
	  name = models.CharField(max_length=200, null=True, blank=True)
	  picture = models.CharField(max_length=250, null=True, blank=True,help_text="a url pointing directly to a preview image of the first video in a course")
	  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', blank=True, null=True)

class Video(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    video_id = models.IntegerField()
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=480)
    duration = models.DecimalField(max_digits=64, decimal_places=2, default=0,help_text="duration of the video")
    picture = models.CharField(max_length=250, blank=True, null=True,help_text="a url pointing directly to a preview image of the video")
    upload_link = models.CharField(max_length=250, blank=True, null=True,help_text="a link that points directly to the video on the vimeo server")
    upload_status = models.CharField(max_length=11, blank=True, null=True,help_text="the upload status of the video. possible values are: in_progress, complete, error")
    transcode_status = models.CharField(max_length=11, blank=True, null=True,help_text="the transcoding status of the video. possible values are: in_progress, complete, error")
    course = models.ForeignKey('video.Course', related_name='videos', blank=True, null=True)

    def __unicode__(self):
      return self.name