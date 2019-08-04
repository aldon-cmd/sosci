from django.forms import ModelForm
from django import forms
from catalogue import models


class CourseForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['name', 'description']


class CourseModuleForm(forms.Form):
    name = forms.CharField(max_length=100)
    duration = forms.CharField(max_length=100)
    chunksize = forms.IntegerField()
    video_file = forms.FileField()

    class Meta:
        model = models.CourseModule       