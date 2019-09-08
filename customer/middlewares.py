import re
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from payroll import models

class LoginRequiredMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.private_urls = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)        

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        # No need to process remaining URLs if user already logged in
        if request.user.is_authenticated():
            return None

        # Requests matching a restricted URL pattern are returned
        # wrapped with the login_required decorator
        for url in self.private_urls:
            if url.match(request.path):
                return login_required(view_func)(request, *view_args, **view_kwargs)

        return None

class AnonymousRequiredMiddleware(object):
    """
    prevents a logged in user from browsing to views like the landing page
    """

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response        
        self.public_urls = tuple(re.compile(url) for url in settings.ANONYMOUS_REQUIRED_URLS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #continue to response if the user is not logged in
        if not request.user.is_authenticated():
           return None

        # An exception match (public_urls) should immediately return None
        for url in self.public_urls:
            if url.match(request.path):
                taxpayername_slug = request.session.get("taxpayername_slug")
                if taxpayername_slug:
                   return HttpResponseRedirect(reverse('dashboard:business-dashboard',kwargs={'taxpayername_slug':taxpayername_slug}))
                else:
                    return redirect("dashboard:business-list")

        # Require login for all non-matching requests
        return None