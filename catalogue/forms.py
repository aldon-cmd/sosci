from django.forms import ModelForm
from django import forms
from catalogue import models


class CourseForm(ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=6,decimal_places=2)
    product_class = forms.ModelChoiceField(queryset=models.ProductClass.objects.all())
    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class']


class CourseModuleForm(forms.Form):
    name = forms.CharField(max_length=100)
    duration = forms.CharField(max_length=100)
    chunksize = forms.IntegerField()
    video_file = forms.FileField()

    class Meta:
        model = models.CourseModule       