from django.conf.urls import url

from video import views

urlpatterns = [
    url(r'^upload/(?P<course_id>\d+)$', views.VimeoVideoUploadFormView.as_view(), name='video-upload-form'),
    url(r'^upload/attempt/(?P<course_id>\d+)$', views.VimeoVideoCreateView.as_view(), name='video-upload-attempt'),
    url(r'^player/(?P<video_id>\d+)$', views.VideoPlayerView.as_view(), name='video-player'),
    url(r'^list/(?P<course_id>\d+)$', views.VideoListView.as_view(), name='video-list'),
    url(r'^create/course$', views.CourseCreateView.as_view(), name='course-create-form'),
    url(r'^course/list$', views.CourseListView.as_view(), name='course-list'),
]