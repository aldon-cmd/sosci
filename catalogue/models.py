from django.db import models
from django.conf import settings
from oscar.apps.catalogue.abstract_models import AbstractProduct

class Product(AbstractProduct):
      name = models.CharField(max_length=200, null=True, blank=True)
      description = models.CharField(max_length=300, null=True, blank=True)
      picture = models.CharField(max_length=250, null=True, blank=True,help_text="a url pointing directly to a preview image of the first video in a course")
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', blank=True, null=True)

class CourseModule(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    video = models.ForeignKey("video.Video", related_name='coursemodules', blank=True, null=True)
    course = models.ForeignKey("catalogue.Product", related_name='coursemodules', blank=True, null=True)

class Enrollment(models.Model):
      course = models.ForeignKey("catalogue.Product", related_name='enrollments', blank=True)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', blank=True)      

from oscar.apps.catalogue.models import *  # noqa isort:skip
