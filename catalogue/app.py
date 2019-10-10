from django.conf.urls import url
from oscar.apps.catalogue import app
from catalogue import views

class CatalogueApplication(app.CatalogueApplication):

    def get_urls(self):
    	
        urlpatterns = [
			    url(r'^detail/(?P<course_id>\d+)$', views.CourseDetailView.as_view(), name='course-detail'),
                url(r'^live/detail/(?P<course_id>\d+)$', views.LiveCourseDetailView.as_view(), name='live-course-detail'),
			    url(r'^enroll/(?P<course_id>\d+)$', views.CourseEnrollmentView.as_view(), name='course-enrollment'),
                url(r'^publish/(?P<course_id>\d+)$', views.PublishCourseView.as_view(), name='publish-course'),
			    url(r'^module/create/(?P<course_id>\d+)$', views.ModuleCreateView.as_view(), name='module-create-form'),
			    url(r'^create$', views.CourseCreateView.as_view(), name='course-create-form'),
                url(r'^live/create$', views.LiveCourseCreateView.as_view(), name='live-course-create-form'),
                url(r'^live/module/create/(?P<course_id>\d+)$', views.LiveModuleCreateView.as_view(), name='live-module-create-form'),
                url(r'^my-courses$', views.MyCoursesListView.as_view(), name='my-course-list'),
                url(r'^my-enrolled-courses$', views.MyEnrolledCoursesListView.as_view(), name='my-enrolled-courses-list'),
			    url(r'^list$', views.CourseListView.as_view(), name='course-list'),
                url(r'^live/list$', views.LiveCourseListView.as_view(), name='live-course-list'),
        ]
        urlpatterns += super(CatalogueApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CatalogueApplication()