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


class TwilioPlayerView(TemplateView):
    template_name = "livestream/player.html"

class TwilioTokenView(View):

    def get(self, request):
        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET

        # Create an Access Token
        token = AccessToken(account_sid, api_key, api_secret)

        # Set the Identity of this token
        token.identity = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
        
        # Grant access to Video
        grant = VideoGrant()
        grant.room = 'room'
        token.add_grant(grant)

        return JsonResponse({'identity':token.identity,'token':token.to_jwt()})