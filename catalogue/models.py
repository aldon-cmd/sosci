from django.db import models
from django.conf import settings
from oscar.apps.catalogue.abstract_models import AbstractProduct
from django.utils.translation import ugettext_lazy as _

class Product(AbstractProduct):
      name = models.CharField(max_length=200, null=True, blank=True)
      description = models.CharField(max_length=300, null=True, blank=True)
      is_published = models.BooleanField(default=False)
      picture = models.CharField(max_length=250, null=True, blank=True,help_text="a url pointing directly to a preview image of the first video in a course")
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', blank=True, null=True)

class CourseModule(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    duration = models.CharField(max_length=200, null=True, blank=True)
    product = models.ForeignKey("catalogue.Product", related_name='coursemodules', blank=True, null=True)

class Enrollment(models.Model):
      product = models.ForeignKey("catalogue.Product", related_name='enrollments', blank=True)
      user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', blank=True)      

from oscar.apps.catalogue.models import *  # noqa isort:skip
