# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string
import random
from django.views import View
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
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
from livestream import mixins

class JitsiMeetRoomView(TemplateView):
    """
    creates a room, token , identity for a host
    """
    template_name = "livestream/jitsi_meet_room.html"


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

class TwilioRoomParticipantView(TemplateView,mixins.CourseRoomMixin):
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
        chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

        course_id = self.kwargs.get('course_id')
        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        course_owner = self.get_owner(course)
        context["course"] = course
        context["owner"] = course_owner

        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)

        # Set the Identity of this token
        token.identity = self.get_identity(self.request)

        
        
        # Grant access to Video
        grant = VideoGrant()
        grant.room = course_id
        token.add_grant(grant)

        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)

        context["token"] = str(token.to_jwt(),'utf-8')
        context["identity"] = token.identity

        return context
  

class TwilioRoomView(TemplateView,mixins.CourseRoomMixin):
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
        chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

        course_id = self.kwargs.get('course_id')
        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        course_owner = self.get_owner(course)
        context["course"] = course
        context["owner"] = course_owner

        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)

        # Set the Identity of this token
        token.identity = self.get_identity(self.request)
        
        # Grant access to Video
        grant = VideoGrant()
        grant.room = course_id
        token.add_grant(grant)

        chat_grant = ChatGrant(service_sid=chat_service_sid)
        token.add_grant(chat_grant)

        auth_token = str(token.to_jwt(),'utf-8')

        """
        https://www.twilio.com/docs/video/api/rooms-resource?code-sample=code-create-a-group-room&code-language=Python&code-sdk-version=6.x
        """       

        try:
            client = Client(account_sid, rest_api_auth_token)
            room = client.video.rooms.create(
                                          # record_participants_on_connect=True,
                                          status_callback=self.request.build_absolute_uri(reverse('instructor:twilio-room-status')),
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
        context["identity"] = token.identity
        context["host_identity"] = self.get_host_identity(course_owner)
        


        return context