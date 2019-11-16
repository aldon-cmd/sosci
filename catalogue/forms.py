from django import forms
from catalogue import models
from tinymce.widgets import TinyMCE

class CourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=6,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Course"))
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class']

class LiveCourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=6,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Live"))
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class']

class LiveCourseModuleForm(forms.ModelForm):

    class Meta:
        model = models.CourseModule
        fields = ['name', 'start_date']


class CourseModuleForm(forms.Form):
    name = forms.CharField(max_length=100)
    duration = forms.CharField(max_length=100)
    chunksize = forms.IntegerField()
    video_file = forms.FileField()