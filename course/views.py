# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from course import models
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from course import forms
# Create your views here.

class CourseListView(ListView):
    template_name = "course/course_list.html"
    paginate_by = 10
    model = models.Course

class CourseCreateView(TemplateView):
    template_name = "course/course_form.html"
    model = models.Course

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)

        context["course_form"]  = forms.CourseForm(prefix="course_form")  # instance= None
        context["coursemodule_formset"] = forms.CourseModuleFormset(queryset=models.CourseModule.objects.none(),prefix="coursemodule_formset")

        return context

    def post(self, request, *args, **kwargs):

        course_form = forms.CourseForm(request.POST,prefix="course_form")
        coursemodule_formset = forms.CourseModuleFormset(request.POST,prefix="coursemodule_formset")
        if course_form.is_valid() and coursemodule_formset.is_valid():
            course = course_form.save(commit=False)
            course.save()

            coursemodule_instances = coursemodule_formset.save(commit=False)
            for obj in coursemodule_instances:
                obj.course = course
            models.CourseModule.objects.bulk_create(coursemodule_instances)

            #clear forms
            course_form = forms.CourseForm(prefix="course_form")
            coursemodule_formset = forms.CourseModuleFormset(queryset=models.CourseModule.objects.none(),prefix="coursemodule_formset")

        return self.render_to_response(self.get_context_data(**{'course_form': course_form, 'coursemodule_formset':coursemodule_formset}))


class CourseDetailView(TemplateView):
    template_name = "course/course_detail.html"

class CourseEnrollmentView(View):

    def post(self, request, *args, **kwargs):
        pass
