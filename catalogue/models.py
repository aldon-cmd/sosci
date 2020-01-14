from django.db import models
from django.conf import settings
from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.utils.translation import ugettext_lazy as _

class Provider(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
      return self.name

class Product(AbstractProduct):
      name = models.CharField(max_length=200, null=True, blank=True)
      start_date = models.DateField(null=True, blank=True)
      start_time = models.TimeField(null=True, blank=True)
      end_time = models.TimeField(null=True, blank=True)
      credit_hour = models.IntegerField(null=True, blank=True)
      description = models.CharField(max_length=10000, null=True, blank=True)
      is_published = models.BooleanField(default=False)
      picture = models.CharField(max_length=250, null=True, blank=True,help_text="a url pointing directly to a preview image of the first video in a course")
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', blank=True, null=True,on_delete=models.CASCADE)
      provider = models.ForeignKey("catalogue.Provider", related_name='products', blank=True, null=True,on_delete=models.CASCADE)      

class CourseModule(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey("catalogue.Product", related_name='coursemodules', blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
      return self.name

class Enrollment(models.Model):
      product = models.ForeignKey("catalogue.Product", related_name='enrollments', blank=True,on_delete=models.CASCADE)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', blank=True,on_delete=models.CASCADE)      

from oscar.apps.catalogue.models import *  # noqa isort:skip
