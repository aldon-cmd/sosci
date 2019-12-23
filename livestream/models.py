# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TwilioRoomStatus(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

class TwilioRoom(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.CharField(max_length=30, null=True, blank=True)
    twilio_room_status = models.ForeignKey("livestream.TwilioRoomStatus", related_name='twiliorooms', blank=True, null=True,on_delete=models.CASCADE)
    product = models.ForeignKey("catalogue.Product", related_name='twiliorooms', blank=True, null=True,on_delete=models.CASCADE)