from django.conf.urls import url
from oscar.apps.catalogue import app
from catalogue import views

class CatalogueApplication(app.CatalogueApplication):

    def get_urls(self):
    	
        urlpatterns = [
			    url(r'^course/details/(?P<course_id>\d+)/$', views.CourseDetailView.as_view(), name='course-detail'),
                url(r'^live/details/(?P<course_id>\d+)/$', views.LiveCourseDetailView.as_view(), name='live-course-detail'),
			    url(r'^enroll/(?P<course_id>\d+)/$', views.CourseEnrollmentView.as_view(), name='course-enrollment'),
			    url(r'^course/create/$', views.CourseCreateView.as_view(), name='course-create-form'),
                url(r'^live/create/$', views.LiveCourseCreateView.as_view(), name='live-course-create-form'),
                url(r'^my-courses/$', views.MyCoursesListView.as_view(), name='my-course-list'),
                url(r'^my-enrolled-courses/$', views.MyEnrolledCoursesListView.as_view(), name='my-enrolled-courses-list'),
                url(r'^my-created-courses/$', views.MyCreatedCoursesListView.as_view(), name='my-created-courses-list'),                
			    url(r'^list/$', views.CourseListView.as_view(), name='course-list'),
                url(r'^live/list/$', views.LiveCourseListView.as_view(), name='live-course-list'),
                url(r'^sme/list/$', views.SmeCourseListView.as_view(), name='sme-course-list'),
        ]
        urlpatterns += super(CatalogueApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CatalogueApplication()