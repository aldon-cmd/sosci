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
from catalogue import mixins
# Create your views here.

class MyCoursesListView(ListView):
    template_name = "catalogue/course_list.html"
    paginate_by = 10
    model = models.Product

class LiveCourseListView(ListView):
    template_name = "catalogue/live_course_list.html"
    paginate_by = 10
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.filter(product_class__name="Live")

class LiveCourseCreateView(CreateView):
    template_name = "catalogue/course_form.html"
    model = models.Product
    form_class = forms.CourseForm

    def form_valid(self, form):
        product = form.instance
        user = self.request.user
        price = form.cleaned_data['price']
        created_product = CatalogueCreator().create_product(user,"Course","Course > Live",product.title,product.description,price,1)
        return HttpResponseRedirect(self.get_success_url(created_product))

    def get_success_url(self,product):

        return reverse('catalogue:live-course-detail', kwargs={'course_id': product.pk})


class LiveCourseDetailView(TemplateView,mixins.EnrollmentMixin):
    template_name = "catalogue/live_course_detail.html"


    def get_context_data(self, **kwargs):
        context = super(LiveCourseDetailView, self).get_context_data(**kwargs)
        context["login_form"] = CustomAuthenticationForm()
        context["course"] = self.get_course()
        if self.request.user.is_authenticated():
           context["is_pending"] = False

        return context

    def get_course(self):
        course_id = self.kwargs.get("course_id")
        return models.Product.objects.filter(pk=course_id).first()

class CourseListView(ListView):
    template_name = "catalogue/course_list.html"
    paginate_by = 10
    model = models.Product

    def get_queryset(self):
        return models.Product.objects.filter(product_class__name="Course")

class CourseCreateView(CreateView):
    template_name = "catalogue/course_form.html"
    model = models.Product
    form_class = forms.CourseForm

    def form_valid(self, form):
        product = form.instance
        user = self.request.user
        price = form.cleaned_data['price']
        created_product = CatalogueCreator().create_product(user,"Course","Course > General",product.title,product.description,price,1)
        return HttpResponseRedirect(self.get_success_url(created_product))

    def get_success_url(self,product):

        return reverse('catalogue:module-create-form', kwargs={'course_id': product.pk})

class PublishCourseView(TemplateView):
    template_name = "catalogue/course_publish.html"

    # def get_success_url(self):

    #     return reverse('course:course-create-form', kwargs={'course_id': self.object.course_id})

    def get_context_data(self, **kwargs):
        context = super(PublishCourseView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["course"] = models.Product.objects.filter(pk=course_id).first()
        context["modules"] = models.CourseModule.objects.filter(product_id=course_id)


        return context

class ModuleCreateView(TemplateView):
    template_name = "catalogue/course_module_form.html"

    # def get_success_url(self):

    #     return reverse('course:course-create-form', kwargs={'course_id': self.object.course_id})

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["form"] = forms.CourseModuleForm()
        context["course"] = models.Product.objects.filter(pk=course_id).first()
        context["modules"] = models.CourseModule.objects.filter(product_id=course_id)


        return context

class CourseDetailView(TemplateView,mixins.EnrollmentMixin):
    template_name = "catalogue/course_detail.html"

    def dispatch(self, request, *args, **kwargs):

        course_id = self.kwargs.get('course_id')
        if request.user.is_authenticated() and self.is_enrolled(request.user,course_id, models):
            
            return http.HttpResponseRedirect(
                    reverse('video:video-player', kwargs={'course_id': course_id}))

        return super(CourseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["login_form"] = CustomAuthenticationForm()
        context["course"] = self.get_course()
        if self.request.user.is_authenticated():
           context["is_pending"] = False

        return context

    def get_course(self):
        course_id = self.kwargs.get("course_id")
        return models.Product.objects.prefetch_related("coursemodules").filter(pk=course_id).first()
        

class CourseEnrollmentView(View):
    template_name = "catalogue/course_enrollment.html"

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action', None)
        course_id = self.kwargs.get("course_id")
        if action == 'enroll' and request.user.is_authenticated():
            if not self.is_enrolled():
               models.Enrollment.objects.create(user=request.user,product_id=course_id)

        return http.HttpResponseRedirect(
                    reverse('catalogue:course-detail', kwargs={'course_id': course_id}))

    def is_enrolled(self):
        user = self.request.user
        course_id = self.kwargs.get("course_id")
        return models.Enrollment.objects.filter(user=user,product_id=course_id).exists()