import oscar.apps.catalogue.apps as apps
from django.conf.urls import url

class CatalogueConfig(apps.CatalogueConfig):
    name = 'catalogue'

    def ready(self):
        super().ready()
        from catalogue import views as catalogue_views
        self.catalogue_views = catalogue_views        
        
    def get_urls(self):

        
        
        urls = [
                url(r'^course/details/(?P<course_id>\d+)/$', self.catalogue_views.CourseDetailView.as_view(), name='course-detail'),
                url(r'^live/details/(?P<course_id>\d+)/$', self.catalogue_views.LiveCourseDetailView.as_view(), name='live-course-detail'),
                url(r'^enroll/(?P<course_id>\d+)/$', self.catalogue_views.CourseEnrollmentView.as_view(), name='course-enrollment'),
                url(r'^course/create/$', self.catalogue_views.CourseCreateView.as_view(), name='course-create-form'),
                url(r'^live/create/$', self.catalogue_views.LiveCourseCreateView.as_view(), name='live-course-create-form'),
                url(r'^my-courses/$', self.catalogue_views.MyCoursesListView.as_view(), name='my-course-list'),
                url(r'^my-enrolled-courses/$', self.catalogue_views.MyEnrolledCoursesListView.as_view(), name='my-enrolled-courses-list'),
                url(r'^my-created-courses/$', self.catalogue_views.MyCreatedCoursesListView.as_view(), name='my-created-courses-list'),                
                url(r'^list/$', self.catalogue_views.CourseListView.as_view(), name='course-list'),
                url(r'^live/list/$', self.catalogue_views.LiveCourseListView.as_view(), name='live-course-list'),
                url(r'^sme/list/$', self.catalogue_views.SmeCourseListView.as_view(), name='sme-course-list'),
        ]

        urls += super().get_urls()

        return self.post_process_urls(urls)    