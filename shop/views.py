# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.list import ListView
from catalogue.utils import Course
from catalogue import models as catalogue_models
from django.views.generic import TemplateView
from django.db.models import Count

class Welcome1View(TemplateView):
    template_name = "shop/welcome1.html"
   
class Welcome2View(TemplateView):
    template_name = "shop/welcome2.html"

class PopularLandingView(ListView):
    template_name = "shop/popular_landing.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(is_published=True).annotate(enrolled_user_count=Count('enrollments__user') ).order_by('-enrolled_user_count')

class RecentLandingView(ListView):
    template_name = "shop/recent_landing.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(is_published=True).order_by('-date_created')        