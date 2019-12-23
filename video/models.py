# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    video_id = models.IntegerField()
    seen = models.BooleanField(default=False,help_text='determines whether a video has been watched or not')    
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=480)
    duration = models.DecimalField(max_digits=64, decimal_places=2, default=0,help_text="duration of the video")
    picture = models.CharField(max_length=250, blank=True, null=True,help_text="a url pointing directly to a preview image of the video")
    upload_link = models.CharField(max_length=250, blank=True, null=True,help_text="a link that points directly to the video on the vimeo server")
    upload_status = models.CharField(max_length=11, blank=True, null=True,help_text="the upload status of the video. possible values are: in_progress, complete, error")
    transcode_status = models.CharField(max_length=11, blank=True, null=True,help_text="the transcoding status of the video. possible values are: in_progress, complete, error")
    module = models.ForeignKey("catalogue.CourseModule", related_name='videos', blank=True, null=True,on_delete=models.CASCADE)
    product = models.ForeignKey('catalogue.Product', related_name='videos', blank=True, null=True,on_delete=models.CASCADE)

    def __unicode__(self):
      return self.name