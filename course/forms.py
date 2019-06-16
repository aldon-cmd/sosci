from django.forms import ModelForm, modelformset_factory
from course import models
from django.forms import modelformset_factory

class CourseForm(ModelForm):
    class Meta:
        model = models.Course
        fields = ['name', 'description']


CourseModuleFormset = modelformset_factory(models.CourseModule,fields=('name','duration'),extra=0)          