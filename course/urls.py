from django.conf.urls import url

from course import views

urlpatterns = [
    url(r'^detail$', views.CourseDetailView.as_view(), name='course-detail'),
    url(r'^create$', views.CourseCreateView.as_view(), name='course-create-form'),
    url(r'^list$', views.CourseListView.as_view(), name='course-list'),
]