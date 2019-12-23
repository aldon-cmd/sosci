from django.conf.urls import url
from catalogue import views as catalogue_views
from livestream import views as livestream_views

app_name = 'instructor'

urlpatterns = [
        url(r'^publish/course/(?P<course_id>\d+)/$', catalogue_views.PublishCourseView.as_view(), name='publish-course'),
	    url(r'^module/create/(?P<course_id>\d+)/$', catalogue_views.ModuleCreateView.as_view(), name='module-create-form'),
        url(r'^live/module/create/(?P<course_id>\d+)/$', catalogue_views.LiveModuleCreateView.as_view(), name='live-module-create-form'),
        url(r'^student/list/$', catalogue_views.StudentListView.as_view(), name='student-list'),	    
	    url(r'^start-session/(?P<course_id>\d+)/$', livestream_views.StartSessionView.as_view(), name='start-session'),
	    url(r'^end-session/(?P<course_id>\d+)/$', livestream_views.EndSessionView.as_view(), name='end-session'),
	    url(r'^room-status/$', livestream_views.TwilioRoomStatusView.as_view(), name='twilio-room-status'),
	    url(r'^room/host/(?P<course_id>\d+)/$', livestream_views.TwilioRoomView.as_view(), name='twilio-room-host'),	    
]

