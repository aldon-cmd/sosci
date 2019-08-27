from django.conf.urls import url
from oscar.apps.catalogue import app
from catalogue import views

class CatalogueApplication(app.CatalogueApplication):

    def get_urls(self):
    	
        urlpatterns = [
			    url(r'^detail/(?P<course_id>\d+)$', views.CourseDetailView.as_view(), name='course-detail'),
			    url(r'^enroll/(?P<course_id>\d+)$', views.CourseEnrollmentView.as_view(), name='course-enrollment'),
			    url(r'^module/create/(?P<course_id>\d+)$', views.ModuleCreateView.as_view(), name='module-create-form'),
			    url(r'^create$', views.CourseCreateView.as_view(), name='course-create-form'),
                url(r'^my-courses$', views.MyCoursesListView.as_view(), name='my=courses-list'),
			    url(r'^list$', views.CourseListView.as_view(), name='course-list'),
        ]
        urlpatterns += super(CatalogueApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)

application = CatalogueApplication()