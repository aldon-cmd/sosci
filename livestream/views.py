# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string
import random
from django.views import View
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from livestream import models
from catalogue import models as catalogue_models
from django import http
from django.urls import reverse
from django.contrib import messages

class StartSessionView(TemplateView):
    """
    creates a room, token , identity for a user
    """
    template_name = "livestream/start_session.html"

class TwilioRoomView(TemplateView):
    """
    creates a room, token , identity for a user
    """
    template_name = "livestream/room.html"



    def dispatch(self, request, *args, **kwargs):


        course_id = self.kwargs.get('course_id',None)

        course = catalogue_models.Product.objects.filter(pk=course_id).first()

        if not self.is_owner(request,course) and not self.room_exists(course_id):

            messages.error(request, 'only the course owner can create a room for a course that they own')

            return http.HttpResponseRedirect(reverse('catalouge:live-course-list'))
    
        return super(TwilioRoomView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(TwilioRoomView, self).get_context_data(**kwargs)

        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET

        course_id = self.kwargs.get('course_id')

        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)

        # Set the Identity of this token
        token.identity = self.request.user.email
        
        # Grant access to Video
        grant = VideoGrant()
        grant.room = course_id
        token.add_grant(grant)

        context["token"] = token.to_jwt()


        return context


    def is_owner(self,request, course):
        """
        check if user owns course
        """
        return request.user.pk == course.user_id

    def room_exists(self,course_id):
        return models.TwilioRoom.objects.filter(name=course_id).exists()             