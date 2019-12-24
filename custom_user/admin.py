# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from custom_user import models as custom_user_models

class UserAdmin(admin.ModelAdmin):
      exclude = ('password',)

admin.site.register(custom_user_models.User,UserAdmin)