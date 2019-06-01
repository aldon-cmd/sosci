# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from video import models
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

class CourseListView(ListView):
    template_name = "course/course_list.html"
    paginate_by = 10
    model = models.Course

class CourseCreateView(CreateView):
    template_name = "course/course_form.html"
    model = models.Course
    fields = ['name']

    def form_valid(self, form):
        form.instance.user_id = self.request.user.pk
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('course:course-list')

class CourseDetailView(TemplateView):
    template_name = "course/course_detail.html"

class CourseEnrollmentView(View):

    def post(self, request, *args, **kwargs):
        pass
