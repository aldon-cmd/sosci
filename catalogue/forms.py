from datetime import datetime
from django import forms
from catalogue import models
from django.forms.widgets import SelectDateWidget


class CourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=12,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Course"))
    description = forms.CharField(widget=forms.Textarea())

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class','credit_hour','provider']

    def clean_title(self):
        return self.cleaned_data['title'].title()

class LiveCourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    start_date = forms.DateField(required=False,widget=SelectDateWidget(attrs=({'class': "input-dropdown"}),years=range(datetime.now().year - 20, datetime.now().year + 1),empty_label=("Year", "Month", "Day")))
    start_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p',attrs=({'type': "time"})))
    end_time = forms.TimeField(widget=forms.TimeInput(format='%I:%M %p',attrs=({'type': "time"})))
    price = forms.DecimalField(max_digits=12,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Live"))
    description = forms.CharField(widget=forms.Textarea())

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class','start_date','start_time','end_time','credit_hour','provider']

    def clean_title(self):
        return self.cleaned_data['title'].title()

class LiveCourseModuleForm(forms.ModelForm):

    class Meta:
        model = models.CourseModule
        fields = ['name', 'start_date']

    def clean_name(self):
        return self.cleaned_data['name'].title()

class CourseModuleForm(forms.Form):
    name = forms.CharField(max_length=100)
    duration = forms.CharField(max_length=100)
    chunksize = forms.IntegerField()
    video_file = forms.FileField()

    def clean_name(self):
        return self.cleaned_data['name'].title()    