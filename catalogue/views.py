# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView
from catalogue import models as catalogue_models
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalogue import forms
from django import http
from customer.forms import CustomAuthenticationForm
from django.views.generic.edit import FormView
from catalogue.utils import CatalogueCreator,Course
from catalogue import mixins
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from partner import models as partner_models

# Create your views here.
class CourseListView(ListView):
    template_name = "catalogue/catalogue_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(is_published=True)

class MyCreatedCoursesListView(ListView):
    """
    list of courses that a user has enrolled in
    """
    template_name = "catalogue/my_created_courses_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(user=self.request.user)

class MyEnrolledCoursesListView(ListView):
    """
    list of courses that a user has enrolled in
    """
    template_name = "catalogue/my_enrolled_courses_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(enrollments__user_id=self.request.user.pk)

class MyCoursesListView(ListView):
    """
    list of courses that a user has enrolled in
    """
    template_name = "catalogue/my_courses_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(Q(enrollments__user_id=self.request.user.pk) | Q(user=self.request.user)).distinct()

class OnDemandCourseListView(ListView):
    template_name = "catalogue/catalogue_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(product_class__name="Course")

class LiveCourseListView(ListView):
    template_name = "catalogue/live_course_list.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(product_class__name="Live")

class LiveCourseUpdateView(UpdateView):
    template_name = "catalogue/course_update_form.html"
    model = catalogue_models.Product
    form_class = forms.LiveCourseForm
    pk_url_kwarg = 'course_id'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(LiveCourseUpdateView, self).get_form_kwargs()
        course_id = self.kwargs.get('course_id')
        stockrecord = partner_models.StockRecord.objects.filter(product_id=course_id).first()

        kwargs['initial'] = {'price': stockrecord.price_excl_tax}
        return kwargs

    def get_success_url(self):
        course_id = self.kwargs.get('course_id')
        return reverse('catalogue:course-detail', kwargs={'course_id': course_id})

    def form_valid(self, form):
        product = form.instance
        price = form.cleaned_data['price']
        stockrecord = partner_models.StockRecord.objects.filter(product_id=product.pk).first()
        stockrecord.price_excl_tax = price
        stockrecord.save()
        product.save()
        return HttpResponseRedirect(self.get_success_url())

class LiveCourseCreateView(CreateView):
    template_name = "catalogue/course_form.html"
    model = catalogue_models.Product
    form_class = forms.LiveCourseForm

    def form_valid(self, form):
        product = form.instance
        user = self.request.user
        price = form.cleaned_data['price']
        created_product = CatalogueCreator().create_product(user,"Live","Course > Live",product.title,product.description,price,1)
        Course().enroll(self.request.user,created_product.pk)
        return HttpResponseRedirect(self.get_success_url(created_product))

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(LiveCourseCreateView, self).get_form_kwargs()
        product_class = catalogue_models.ProductClass.objects.filter(name = "Live").first()

        kwargs['initial'] = {'product_class': product_class.pk}
        return kwargs

    def get_success_url(self,product):

        return reverse('instructor:live-module-create-form', kwargs={'course_id': product.pk})


class LiveModuleCreateView(CreateView):
    template_name = "catalogue/live_course_module_form.html"
    form_class = forms.LiveCourseModuleForm

    def get_success_url(self):
        course_id = self.kwargs.get('course_id')
        return reverse('instructor:live-module-create-form', kwargs={'course_id': course_id})

    def form_valid(self, form):
        course_module = form.instance
        course_id = self.kwargs.get('course_id')
        course = catalogue_models.Product.objects.filter(pk=course_id).first()
        course_module.product = course
        course_module.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(LiveModuleCreateView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["course"] = catalogue_models.Product.objects.filter(pk=course_id).first()
        context["modules"] = catalogue_models.CourseModule.objects.filter(product_id=course_id)


        return context

class LiveCourseDetailView(TemplateView):
    template_name = "catalogue/live_course_detail.html"
    
    def get_context_data(self, **kwargs):
        course_id = self.kwargs.get("course_id")
        context = super(LiveCourseDetailView, self).get_context_data(**kwargs)
        context["login_form"] = CustomAuthenticationForm()
        context["course"] = Course().get_course(course_id)
        context["is_enrolled"] = Course().is_enrolled(self.request.user,course_id)


        return context


class CourseUpdateView(UpdateView):
    template_name = "catalogue/course_update_form.html"
    model = catalogue_models.Product
    form_class = forms.CourseForm
    pk_url_kwarg = 'course_id'

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(CourseUpdateView, self).get_form_kwargs()
        course_id = self.kwargs.get('course_id')
        stockrecord = partner_models.StockRecord.objects.filter(product_id=course_id).first()

        kwargs['initial'] = {'price': stockrecord.price_excl_tax}
        return kwargs

    def form_valid(self, form):
        product = form.instance
        price = form.cleaned_data['price']
        stockrecord = catalogue_models.StockRecord.objects.filter(product_id=product.pk).first()
        stockrecord.price_excl_tax = price
        stockrecord.save()
        product.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        course_id = self.kwargs.get('course_id')
        return reverse('catalogue:course-detail', kwargs={'course_id': course_id})


class CourseCreateView(CreateView):
    template_name = "catalogue/course_form.html"
    model = catalogue_models.Product
    form_class = forms.CourseForm

    def form_valid(self, form):
        product = form.instance
        user = self.request.user
        price = form.cleaned_data['price']
        created_product = CatalogueCreator().create_product(user,"Course","Course > General",product.title,product.description,price,1)
        Course().enroll(self.request.user,created_product.pk)
        return HttpResponseRedirect(self.get_success_url(created_product))

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(CourseCreateView, self).get_form_kwargs()
        product_class = catalogue_models.ProductClass.objects.filter(name = "Course").first()

        kwargs['initial'] = {'product_class': product_class.pk}
        return kwargs
        
    def get_success_url(self,product):

        return reverse('instructor:module-create-form', kwargs={'course_id': product.pk})

class PublishCourseView(TemplateView):
    template_name = "catalogue/course_publish.html"

    # def get_success_url(self):

    #     return reverse('course:course-create-form', kwargs={'course_id': self.object.course_id})

    def dispatch(self, request, *args, **kwargs):

        course_id = self.kwargs.get('course_id')
        course = catalogue_models.Product.objects.prefetch_related("coursemodules").filter(pk=course_id).first()


        #cannot publish a course that has no modules
        if not course.coursemodules.exists():

           return http.HttpResponseRedirect(
                    reverse('instructor:module-create-form', kwargs={'course_id': course_id}))



        return super(PublishCourseView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):    
            action = self.request.POST.get('action', None)
            course_id = self.kwargs.get('course_id')
            course = catalogue_models.Product.objects.filter(pk=course_id).first()
            if action == 'publish':
                course.is_published = True
                course.save()

            return http.HttpResponseRedirect(
                    reverse('catalogue:my-course-list'))

    def get_context_data(self, **kwargs):
        context = super(PublishCourseView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["course"] = catalogue_models.Product.objects.filter(pk=course_id).first()
        context["modules"] = catalogue_models.CourseModule.objects.filter(product_id=course_id)


        return context

class ModuleCreateView(TemplateView):
    template_name = "catalogue/course_module_form.html"

    # def get_success_url(self):

    #     return reverse('course:course-create-form', kwargs={'course_id': self.object.course_id})

    def get_context_data(self, **kwargs):
        context = super(ModuleCreateView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context["form"] = forms.CourseModuleForm()
        context["course"] = catalogue_models.Product.objects.filter(pk=course_id).first()
        context["modules"] = catalogue_models.CourseModule.objects.filter(product_id=course_id)

        return context

class CourseDetailView(TemplateView):

    def get_template_names(self):

        
        course_id = self.kwargs.get('course_id')
        course = catalogue_models.Product.objects.select_related("product_class").filter(pk=course_id).first()
        if self.template_name:
            return [self.template_name]

        if course.product_class.name == "Live":
           return ["catalogue/live_course_detail.html"]
        elif course.product_class.name == "Course":
            return ["catalogue/course_detail.html"]
        else:
            raise ImproperlyConfigured(
                "this page requires a product class to be set")

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        course_id = self.kwargs.get("course_id")
        context["login_form"] = CustomAuthenticationForm()
        context["course"] = Course().get_course(course_id)

        context["is_enrolled"] = Course().is_enrolled(self.request.user,course_id)

        return context        

class CourseEnrollmentView(TemplateView):
    template_name = "catalogue/course_enrollment.html"

    def post(self, request, *args, **kwargs):
        action = self.request.POST.get('action', None)
        course_id = self.kwargs.get("course_id")
        if action == 'enroll' and request.user.is_authenticated:
            if not Course().is_enrolled(request.user,course_id):
               Course().enroll(request.user,course_id)

        return http.HttpResponseRedirect(
                    reverse('catalogue:course-detail', kwargs={'course_id': course_id}))

class StudentListView(ListView):
    template_name = "catalogue/student_list.html"
    paginate_by = 10
    model = catalogue_models.Product