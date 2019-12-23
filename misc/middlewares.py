import re
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from payroll import models

class ReadOnlyMiddleware(object):
    """
    middleware that checks to see if a user is a part of a group that can make changes
    """

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response        
        self.public_urls = tuple(re.compile(url) for url in settings.PUBLIC_ACTION_URLS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        # An exception match (public_urls) should immediately return None
        for url in self.public_urls:
            if url.match(request.path):
                return None

        taxpayername_slug = request.session.get("taxpayername_slug")

        #redirect to the current page if the user is not in a group that can make changes
        if request.method == "POST" and not request.user.groups.filter(name__in=['Admin','Officer'],business__taxpayername_slug=taxpayername_slug).exists():

           messages.error(request, "You are not allowed to make changes")
           return redirect(request.META.get('HTTP_REFERER', 'dashboard:business-dashboard'))


        # Require login for all non-matching requests
        return None

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
        self.public_urls = tuple(re.compile(url) for url in settings.PUBLIC_URLS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        # No need to process remaining URLs if user already logged in
        if request.user.is_authenticated:
            return None

        # An exception match (public_urls) should immediately return None
        for url in self.public_urls:
            if url.match(request.path):
                return None

        # Require login for all non-matching requests
        return login_required(view_func)(request, *view_args, **view_kwargs)

class AnonymousRequiredMiddleware(object):
    """
    prevents a logged in user from browsing to views like the landing page
    """

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response        
        self.public_urls = tuple(re.compile(url) for url in settings.PRIVATE_ANONYMOUS_URLS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #continue to response if the user is not logged in
        if not request.user.is_authenticated:
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

class BusinessOwnerMiddleware(object):
    """
    must follow after the LoginRequiredMiddleware which will short circuit if the user is not logged
    in
    """
    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.public_urls = tuple(re.compile(url) for url in settings.PUBLIC_BUSINESS_URLS) 

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        for url in self.public_urls:
            if url.match(request.path):
                return None        

        #user visits url that contains taxpayername_slug
        taxpayername_slug = view_kwargs.get("taxpayername_slug")        
        if taxpayername_slug is None:
            #user visits a url that does not contain a taxpayername_slug
            taxpayername_slug = request.session.get("taxpayername_slug")
            if taxpayername_slug is None:
               return redirect("dashboard:business-list")
            
        if taxpayername_slug and not request.user.businesses.filter(taxpayername_slug=taxpayername_slug).exists():
            return redirect("dashboard:business-list")

        return None


class PayPeriodRequiredMiddleware(object):
    """
    must follow after the LoginRequiredMiddleware which will short circuit if the user is not logged
    in
    """
    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.public_urls = tuple(re.compile(url) for url in settings.PUBLIC_PAYPERIOD_URLS) 

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        for url in self.public_urls:
            if url.match(request.path):
                return None        



        #user visits url that contains taxpayername_slug
        taxpayername_slug = view_kwargs.get("taxpayername_slug")        
        if taxpayername_slug is None:
            #user visits a url that does not contain a taxpayername_slug
            taxpayername_slug = request.session.get("taxpayername_slug")
            if taxpayername_slug is None:
               return None
                       
        if not models.PayPeriod.objects.filter(payperiodtype__payperiod__in=["Monthly Period","Weekly Period","Fortnightly Period"],business__taxpayername_slug=taxpayername_slug).exists():

            return HttpResponseRedirect(reverse('dashboard:payperiod-create-form',kwargs={'taxpayername_slug':taxpayername_slug}))
            

        return None             