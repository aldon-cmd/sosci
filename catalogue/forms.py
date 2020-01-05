from django import forms
from catalogue import models


class CourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=12,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Course"))
    description = forms.CharField(widget=forms.Textarea())

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class']

    def clean_title(self):
        return self.cleaned_data['title'].title()

class LiveCourseForm(forms.ModelForm):
    CHOICES = (
        ("Product Class", "Course"),
    )
    price = forms.DecimalField(max_digits=12,decimal_places=2)
    product_class = forms.ModelChoiceField(widget=forms.HiddenInput,queryset=models.ProductClass.objects.filter(name="Live"))
    description = forms.CharField(widget=forms.Textarea())

    class Meta:

        model = models.Product
        fields = ['title', 'description','product_class']

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