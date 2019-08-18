# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.db.models import DecimalField, Count, Sum, When, Case, Q, Prefetch
from django.contrib.auth.models import Group
from django.contrib.auth import views as auth_views
from customer.forms import CustomAuthenticationForm,EmailUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django.urls import reverse


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
        return HttpResponseRedirect(self.request.path_info)

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
        return redirect('catalogue:course-list')

class RegistrationModalView(FormView):
    form_class = EmailUserCreationForm
    template_name = 'customer/registration_modal.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return HttpResponseRedirect(self.request.path_info)

    def form_invalid(self, form):
        response = super(RegistrationModalView, self).form_invalid(form)
        response.status_code = 400
        return response

class UserRegistrationView(FormView):
    form_class = EmailUserCreationForm
    template_name = 'customer/user_registration.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return redirect('/')