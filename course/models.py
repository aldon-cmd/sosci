# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.
class Course(models.Model):
	  name = models.CharField(max_length=200, null=True, blank=True)
	  description = models.CharField(max_length=300, null=True, blank=True)
	  picture = models.CharField(max_length=250, null=True, blank=True,help_text="a url pointing directly to a preview image of the first video in a course")
	  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', blank=True, null=True)

class CourseModule(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	course = models.ForeignKey("course.Course", related_name='coursemodules', blank=True, null=True)

class Enrollment(models.Model):
	  course = models.ForeignKey("course.Course", related_name='enrollments', blank=True, null=True)
	  user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', blank=True, null=True)