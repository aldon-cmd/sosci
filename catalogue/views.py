# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.list import ListView
from video import models


class CatalogueListView(ListView):
    template_name = "catalogue/catalogue_list.html"
    paginate_by = 10
    model = models.Video