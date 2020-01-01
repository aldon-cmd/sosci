from django.urls import re_path
from catalogue import views as catalogue_views
from livestream import views as livestream_views

app_name = 'instructor'

urlpatterns = [
        re_path(r'^course/update/(?P<course_id>\d+)/$', catalogue_views.CourseUpdateView.as_view(), name='course-update-form'),
        re_path(r'^live/course/update/(?P<course_id>\d+)/$', catalogue_views.LiveCourseUpdateView.as_view(), name='live-course-update-form'),
        re_path(r'^publish/course/(?P<course_id>\d+)/$', catalogue_views.PublishCourseView.as_view(), name='publish-course'),
	    re_path(r'^module/create/(?P<course_id>\d+)/$', catalogue_views.ModuleCreateView.as_view(), name='module-create-form'),
        re_path(r'^live/module/create/(?P<course_id>\d+)/$', catalogue_views.LiveModuleCreateView.as_view(), name='live-module-create-form'),
        re_path(r'^student/list/$', catalogue_views.StudentListView.as_view(), name='student-list'),	    
	    re_path(r'^start-session/(?P<course_id>\d+)/$', livestream_views.StartSessionView.as_view(), name='start-session'),
	    re_path(r'^end-session/(?P<course_id>\d+)/$', livestream_views.EndSessionView.as_view(), name='end-session'),
	    re_path(r'^room-status/$', livestream_views.TwilioRoomStatusView.as_view(), name='twilio-room-status'),
	    re_path(r'^room/host/(?P<course_id>\d+)/$', livestream_views.TwilioRoomView.as_view(), name='twilio-room-host'),	    
]

