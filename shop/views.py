# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.list import ListView
from catalogue.utils import Course
from catalogue import models as catalogue_models

class LandingView(ListView):
    template_name = "shop/landing.html"
    paginate_by = 10
    model = catalogue_models.Product

    def get_queryset(self):
        return Course().get_courses().filter(is_published=True)