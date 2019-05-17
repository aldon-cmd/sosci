from django.conf.urls import url

from course import views

urlpatterns = [
    url(r'^create$', views.CourseCreateView.as_view(), name='course-create-form'),
    url(r'^list$', views.CourseListView.as_view(), name='course-list'),
]