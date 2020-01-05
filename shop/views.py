# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.list import ListView
from catalogue.utils import Course
from catalogue import models as catalogue_models
from django.views.generic import TemplateView


class Welcome1View(TemplateView):
    template_name = "shop/welcome1.html"
   
class Welcome2View(TemplateView):
    template_name = "shop/welcome2.html"

class LandingView(ListView):
    template_name = "shop/landing.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(is_published=True)