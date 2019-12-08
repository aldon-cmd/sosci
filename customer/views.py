# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from customer.forms import CustomAuthenticationForm,EmailUserCreationForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login as auth_login

from django.urls import reverse
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import get_object_or_404

from django.http import Http404
from django.contrib import messages
from django.utils import timezone
import hashlib, datetime, random
from django.contrib.sites.shortcuts import get_current_site
from customer.models import CommunicationEventType
from customer.utils import Dispatcher
from django.shortcuts import render
from customer import mixins

class LogoutView(auth_views.LogoutView):


    def get(self, request):
        logout(request)

        return redirect('/')


class LoginModalView(auth_views.LoginView):
    template_name = 'customer/login_modal.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):

        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponse(status=200)

    def form_invalid(self, form):
        response = super(LoginModalView, self).form_invalid(form)
        response.status_code = 400
        return response

class LoginView(auth_views.LoginView):
    template_name = 'customer/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):

        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return redirect('catalogue:my-course-list')

class RegistrationModalView(mixins.RegisterUserMixin,FormView):
    form_class = EmailUserCreationForm
    template_name = 'customer/registration_modal.html'

    def form_valid(self, form):
        self.register_user(form)
        return HttpResponse(status=200)

    def form_invalid(self, form):
        response = super(RegistrationModalView, self).form_invalid(form)
        response.status_code = 400
        return response

class UserRegistrationView(mixins.RegisterUserMixin,FormView):
    form_class = EmailUserCreationForm
    template_name = 'customer/user_registration.html'

    def form_valid(self, form):
        self.register_user(form)
        return HttpResponseRedirect(reverse('customer:email-confirm-user'))


class ConfirmUser(TemplateView):
    template_name = 'customer/confirm_user.html'

    def get(self, request, *args, **kwargs):
        #check if user is already logged in and if he is redirect him to some other url, e.g. home
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect(reverse('index'))

        # check if there is UserProfile which matches the activation key (if not then display 404)

        if 'activation_key' in self.kwargs:
            try:
                user = get_object_or_404(get_user_model(), activation_key=self.kwargs.get('activation_key',''))

                if user.is_active == True:
                   messages.success(request,"This user account has already been activated")
                   return HttpResponseRedirect(reverse('catalogue:course-list'))

                #check if the activation key has expired, if it hase then render confirm_expired.html
                if user.key_expires < timezone.now():
                    email = user.email
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
                    activation_key = hashlib.sha1(salt+email).hexdigest()            
                    key_expires = datetime.datetime.today() + datetime.timedelta(2)

                    user.activation_key = activation_key
                    user.key_expires = key_expires
                    user.save()
                    messages.error(request,"This link has expired. Please try sending the confirmation email again")
                    return super(ConfirmUser, self).get(request, *args, **kwargs)
                user.is_active = True
                user.save()

                #have to set backend before login
                user.backend = settings.AUTHENTICATION_BACKENDS[0]
                login(self.request, user)
                return HttpResponseRedirect(reverse('catalogue:course-list'))
            except Http404:

                 return super(ConfirmUser, self).get(request, *args, **kwargs)

        if 'resend' in self.kwargs:
            return super(ConfirmUser, self).get(request, *args, **kwargs)


        ctx = self.get_context_data()
        #a resend form is displayed when a response is returned before this check_email variable is set
        ctx['check_email'] = True
        return render(self.request, self.template_name,ctx)


    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action', None)
        if action == 'resend':
            email = self.request.POST.get('email', None)
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            try:
                user = get_object_or_404(get_user_model(), email=email)
                user.activation_key = activation_key
                user.key_expires = key_expires
                user.save()
            except Http404:
                 messages.error(request,"A user with that email does not exist")
                 return super(ConfirmUser, self).get(request, *args, **kwargs)              
            
            mixins.RegisterUserMixin().send_confirmation_email(user, self.request)
            return HttpResponseRedirect(reverse('customer:email-confirmation-sent'))
        return super(ConfirmUser, self).post(request, *args, **kwargs)

class ConfirmationSuccess(TemplateView):
    template_name = 'customer/confirmation_success.html'            

class ConfirmationSent(TemplateView):
    template_name = 'customer/confirmation_sent.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'customer/registration/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'customer/registration/password_reset_confirm.html'

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'customer/registration/password_reset_complete.html'

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'customer/registration/password_reset_form.html'       