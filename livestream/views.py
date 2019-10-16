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
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from custom_user import models as user_models

class EndSessionView(View):

    def post(self, request, **kwargs):
        account_sid = settings.TWILIO_ACCOUNT_SID
        rest_api_auth_token = settings.TWILIO_REST_API_AUTH_TOKEN

        try:

           client = Client(account_sid, rest_api_auth_token)
           room_sid = request.POST.get("room_sid")
           client.video.rooms(room_sid).update(status='completed')
           return   HttpResponse(status=200)        
            
        except TwilioRestException as e:
            return HttpResponse(status=500)

class StartSessionView(TemplateView):
    """
    creates a room, token , identity for a user
    """
    template_name = "livestream/start_session.html"

class TwilioRoomStatusView(View):
    """

    """


    def post(self, request, **kwargs):

        return HttpResponse(status=204)

class TwilioRoomParticipantView(TemplateView):
    """
    creates a room, token , identity for a participant
    """
    template_name = "livestream/room.html"



    def dispatch(self, request, *args, **kwargs):


        course_id = self.kwargs.get('course_id',None)

        course = catalogue_models.Product.objects.filter(pk=course_id).first()

        if not self.is_owner(request,course) and not self.room_exists(course_id):

            messages.error(request, 'This course is not live yet, check back later')

            return http.HttpResponseRedirect(reverse('catalogue:live-course-list'))
    
        return super(TwilioRoomParticipantView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(TwilioRoomParticipantView, self).get_context_data(**kwargs)


        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY_SID
        api_secret = settings.TWILIO_API_SECRET

        course_id = self.kwargs.get('course_id')
        context["owner"] = self.get_owner(course_id)

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

    def get_owner(course_id):

        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        owner = user_models.User.objects.filter(pk=course.user_id).first()

        return owner

    def is_owner(self,request, course):
        """
        check if user owns course
        """
        return request.user.pk == course.user_id

    def room_exists(self,course_id):
        return models.TwilioRoom.objects.filter(name=course_id,twilio_room_status__name="Active").exists()   



class TwilioRoomView(TemplateView):
    """
    creates a room, token , identity for a host
    """
    template_name = "livestream/room.html"



    # def dispatch(self, request, *args, **kwargs):


    #     course_id = self.kwargs.get('course_id',None)

    #     course = catalogue_models.Product.objects.filter(pk=course_id).first()

    #     if not self.is_owner(request,course):

    #         messages.error(request, 'only the course owner can create a room for a course that they own')

    #         return http.HttpResponseRedirect(reverse('catalogue:live-course-list'))
    
    #     return super(TwilioRoomView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(TwilioRoomView, self).get_context_data(**kwargs)

        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY_SID
        api_secret = settings.TWILIO_API_SECRET
        rest_api_auth_token = settings.TWILIO_REST_API_AUTH_TOKEN

        course_id = self.kwargs.get('course_id')
        context["owner"] = self.get_owner(course_id)

        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)

        # Set the Identity of this token
        token.identity = self.request.user.email
        
        # Grant access to Video
        grant = VideoGrant()
        grant.room = course_id
        token.add_grant(grant)

        auth_token = token.to_jwt()

        """
        https://www.twilio.com/docs/video/api/rooms-resource?code-sample=code-create-a-group-room&code-language=Python&code-sdk-version=6.x
        """       

        try:
            client = Client(account_sid, rest_api_auth_token)
            room = client.video.rooms.create(
                                          record_participants_on_connect=True,
                                          status_callback=self.request.build_absolute_uri(reverse('live:twilio-room-status')),
                                          type='group',
                                          unique_name=course_id
                                      )
            #keep track of the status of the room
            twilio_room_status = models.TwilioRoomStatus.objects.filter(name="Active").first()
            twilio_room = models.TwilioRoom.objects.filter(name=course_id).first()
            twilio_room.twilio_room_status = twilio_room_status
            twilio_room.end_time = room.end_time
            twilio_room.save()            
            
        except TwilioRestException as e:
               message = e.msg
               code = e.code
               room = models.TwilioRoom.objects.filter(name=course_id).first()
               context["end_time"] = room.end_time


        context["token"] = auth_token
        


        return context

    def get_owner(course_id):

        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        owner = user_models.User.objects.filter(pk=course.user_id).first()

        return owner

    def is_owner(self,request, course):
        """
        check if user owns course
        """
        return request.user.pk == course.user_id