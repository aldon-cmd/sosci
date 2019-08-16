# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from customer.forms import CustomAuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

class LandingView(auth_views.LoginView):
    template_name = "promotions/landing.html"
    form_class = CustomAuthenticationForm

    def form_valid(self, form):

        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return redirect('course:course-list')    
