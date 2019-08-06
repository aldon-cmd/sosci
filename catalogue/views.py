# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from catalogue import models
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalogue import forms
from django import http
from customer.forms import CustomAuthenticationForm
from django.views.generic.edit import FormView
from catalogue.utils import CatalogueCreator
# Create your views here.

class CourseListView(ListView):
    template_name = "catalogue/course_list.html"
    paginate_by = 10
    model = models.Product

class CourseCreateView(CreateView):
    template_name = "catalogue/course_form.html"
    model = models.Product
    form_class = forms.CourseForm

    def form_valid(self, form):
        product = form.instance
        CatalogueCreator().create_product("Course","Course > General",product.title,product.description,1.00,1)
        return super(CourseCreateView, self).form_valid(form)

    def get_success_url(self):

        return reverse('catalogue:module-create-form', kwargs={'course_id': self.object.id})

class ModuleCreateView(TemplateView):
    template_name = "catalogue/course_module_form.html"

    # def get_success_url(self):

    #     return reverse('course:course-create-form', kwargs={'course_id': self.object.course_id})

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["form"] = forms.CourseModuleForm()
        context["course"] = models.Product.objects.filter(pk=course_id).first()
        context["modules"] = models.CourseModule.objects.filter(course_id=course_id)


        return context

class CourseDetailView(TemplateView):
    template_name = "catalogue/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["login_form"] = CustomAuthenticationForm()
        context["course"] = self.get_course()
        if self.request.user.is_authenticated():
           context["is_enrolled"] = self.is_enrolled()

        return context

    def get_course(self):
        course_id = self.kwargs.get("course_id")
        return models.Product.objects.prefetch_related("coursemodules").filter(pk=course_id).first()
        
    def is_enrolled(self):
        user = self.request.user
        course_id = self.kwargs.get("course_id")
        return models.Enrollment.objects.filter(user=user,course_id=course_id).exists()

class CourseEnrollmentView(View):
    template_name = "catalogue/course_enrollment.html"

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action', None)
        course_id = self.kwargs.get("course_id")
        if action == 'enroll' and request.user.is_authenticated():
            if not self.is_enrolled():
               models.Enrollment.objects.create(user=request.user,course_id=course_id)

        return http.HttpResponseRedirect(
                    reverse('catalogue:course-detail', kwargs={'course_id': course_id}))

    def is_enrolled(self):
        user = self.request.user
        course_id = self.kwargs.get("course_id")
        return models.Enrollment.objects.filter(user=user,course_id=course_id).exists()