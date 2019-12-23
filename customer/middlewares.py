import re
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from catalogue.utils import Course
from catalogue import models as catalogue_models

class OwnerRequiredMiddleware(object):

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.course_owner_urls = tuple(re.compile(url) for url in settings.COURSE_OWNER_REQUIRED_URLS)        

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #check if user visits url that contains course_id
        course_id = view_kwargs.get("course_id")

        if not course_id:
            return None

        course = catalogue_models.Product.objects.filter(pk=course_id).first()        

        for url in self.course_owner_urls:
            if url.match(request.path) and not Course().is_owner(course,request.user) :
                return redirect(reverse('catalogue:course-list'))                

        return None

class CourseEnrolledMiddleware(object):

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.enrollment_public_urls = tuple(re.compile(url) for url in settings.ENROLLMENT_PUBLIC_URLS)        

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #check if user visits url that contains course_id
        course_id = view_kwargs.get("course_id")        

        for url in self.enrollment_public_urls:
            if url.match(request.path):
                return None
                
        if course_id and not Course().is_enrolled(request.user,course_id):
           return redirect(reverse('catalogue:course-detail',kwargs={'course_id':course_id}))


        return None


class CourseExistsMiddleware(object):

    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response   

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #check if user visits url that contains course_id
        course_id = view_kwargs.get("course_id")        
               
        if course_id and not Course().exists(course_id):
           return redirect(reverse('catalogue:course-list'))

        return None

class CoursePublishedMiddleware(object):
    def __init__(self,get_response=None):
        # One-time configuration and initialization.
        self.get_response = get_response   

    def __call__(self, request):
        self.course_published_public_urls = tuple(re.compile(url) for url in settings.COURSE_PUBLISHED_PUBLIC_URLS) 
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #check if user visits url that contains course_id
        course_id = view_kwargs.get("course_id")        
       

        for url in self.course_published_public_urls:
            if url.match(request.path):
                return None
                               
        if course_id and not Course().is_published(course_id):
           return redirect(reverse('instructor:publish-course',kwargs={'course_id':course_id}))

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
        self.private_urls = tuple(re.compile(url) for url in settings.LOGIN_REQUIRED_URLS)        

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        # No need to process remaining URLs if user already logged in
        if request.user.is_authenticated:
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
        self.anonymous_urls = tuple(re.compile(url) for url in settings.ANONYMOUS_REQUIRED_URLS)

    def __call__(self, request):

        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):        

        #continue to response if the user is not logged in
        if not request.user.is_authenticated:
           return None

        # An exception match (public_urls) should immediately return None
        for url in self.anonymous_urls:
            if url.match(request.path) and request.user.is_authenticated:
               return redirect("catalogue:course-list")

        # Require login for all non-matching requests
        return None