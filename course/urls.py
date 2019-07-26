from django.conf.urls import url

from course import views

urlpatterns = [
    url(r'^detail/(?P<course_id>\d+)$', views.CourseDetailView.as_view(), name='course-detail'),
    url(r'^enroll/(?P<course_id>\d+)$', views.CourseEnrollmentView.as_view(), name='course-enrollment'),
    url(r'^module/create/(?P<course_id>\d+)$', views.ModuleCreateView.as_view(), name='module-create-form'),
    url(r'^create$', views.CourseCreateView.as_view(), name='course-create-form'),
    url(r'^list$', views.CourseListView.as_view(), name='course-list'),
]