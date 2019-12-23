# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models

from oscar.apps.customer.abstract_models import AbstractUser


class User(AbstractUser):
    userrole = models.ForeignKey("custom_user.UserRole", related_name='users', blank=True, null=True,on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    
class UserRole(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
      return self.name